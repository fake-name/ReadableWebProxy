

from sqlalchemy import func

import WebMirror.OutputFilters.FilterBase

import WebMirror.OutputFilters.util.MessageConstructors  as msgpackers
from WebMirror.OutputFilters.util.TitleParsers import extractTitle

import WebMirror.SpecialCase

from . import NUBaseFilter

import bs4
import re
import calendar
import datetime
import time
import json
import pprint
import common.util.WebRequest
import bleach
import multiprocessing
import common.database as db

MIN_RATING = 5


def get_count(q):
	count_q = q.statement.with_only_columns([func.count()]).order_by(None)
	count = q.session.execute(count_q).scalar()
	return count




def upsertNuItem(raw_cur, itemparams):
	required_args = [
		'seriesname',
		'releaseinfo',
		'groupinfo',
		'referrer',
		'outbound_wrapper',
		'first_seen',
		'release_date',
		]

	assert all([key in itemparams for key in required_args])
	assert itemparams['referrer'] != 'http://www.novelupdates.com/'
	assert itemparams['referrer'] != 'http://www.novelupdates.com'

	#  Fucking huzzah for ON CONFLICT!
	cmd = """
			INSERT INTO
				nu_release_item
				(seriesname, releaseinfo, groupinfo, referrer, outbound_wrapper, first_seen, release_date, validated, fetch_attempts)
			VALUES
				(%(seriesname)s, %(releaseinfo)s, %(groupinfo)s, %(referrer)s, %(outbound_wrapper)s, %(first_seen)s, %(release_date)s, %(validated)s, %(fetch_attempts)s)
			ON CONFLICT (outbound_wrapper) DO NOTHING
				;
			""".replace("	", " ").replace("\n", " ")

	# Forward-data the next walk, time, rather then using now-value for the thresh.
	data = {
			'seriesname'       : itemparams['seriesname'],
			'releaseinfo'      : itemparams['releaseinfo'],
			'groupinfo'        : itemparams['groupinfo'],
			'referrer'         : itemparams['referrer'],
			'outbound_wrapper' : itemparams['outbound_wrapper'],
			'release_date'     : itemparams['release_date'],
			'first_seen'       : itemparams['first_seen'],
			'validated'        : False,
			'fetch_attempts'   : 0,
		}

	raw_cur.execute(cmd, data)
	return raw_cur.rowcount


class NUSeriesPageProcessor(NUBaseFilter.NuBaseFilter):


	wanted_mimetypes = [

							'text/html',
						]
	want_priority    = 90

	loggerPath = "Main.Filter.NoveUpdates.Page"
	statsd_prefix = 'ReadableWebProxy.Nu.PageProcessor'

	@staticmethod
	def wantsUrl(url):
		if re.search(r"^https?://(?:www\.)?novelupdates\.com/series/.+/?$", url):
			print("NUSeriesPageProcessor Wants url: '%s'" % url)
			return True
		return False

	def __init__(self, **kwargs):

		self.is_beta    = False
		self.kwargs     = kwargs

		self.pageUrl    = kwargs['pageUrl']

		self.content    = kwargs['pgContent']
		self.type       = kwargs['type']
		self.wg         = kwargs['wg']

		self.log.info("Processing NovelUpdates series page")
		super().__init__(**kwargs)


		self.raw_cur = self.db_sess.connection().connection.cursor()


##################################################################################################################################
##################################################################################################################################
##################################################################################################################################


	def extractSeriesReleases(self, seriesPageUrl, soup):

		titletg  = soup.find("h4", class_='seriestitle')
		if not titletg:
			titletg  = soup.find("div", class_='seriestitlenu')
		altnametg  = soup.find("div", id='editassociated')
		descrtg  = soup.find("div", id='editdescription')

		link_sets = {
			'authortg'        : soup.find("div", id='showauthors'),
			'artisttg'        : soup.find("div", id='showartists'),
			'langtg'          : soup.find("div", id='showlang'),
			'genretg'         : soup.find("div", id='seriesgenre'),
			'tagstg'          : soup.find("div", id='showtags'),
			'typetg'          : soup.find("div", id='showtype'),
			'orig_pub_tg'     : soup.find("div", id='showopublisher'),
			'eng_pub_tg'      : soup.find("div", id='showepublisher'),
		}

		text_sets = {
			'transcompletetg' : soup.find("div", id='showtranslated'),
			'yeartg'          : soup.find("div", id='edityear'),
			'coostatustg'     : soup.find("div", id='editstatus'),
			'licensedtg'      : soup.find("div", id='showlicensed'),
			}

		if not titletg:
			self.log.warn("Could not find item title!")
			print(soup)
			return []
		if not altnametg:
			self.log.warn("Could not find alt-name container tag!")
			return []
		if not descrtg:
			self.log.warn("Could not find description container tag!")
			return []

		data_sets = {}
		for key in list(link_sets.keys()):
			if not link_sets[key]:
				self.log.warn("Could not find tag for name: '%s'", key)
				return []
			data_sets[key] = [tag.get_text() for tag in link_sets[key].find_all("a")]

		for key in list(text_sets.keys()):
			if not text_sets[key]:
				self.log.warn("Could not find tag for name: '%s'", key)
				return []
			data_sets[key] = [tmp.strip() for tmp in text_sets[key].contents if isinstance(tmp, bs4.NavigableString)]

		title  = titletg.get_text().strip()

		data_sets['title'] = title
		data_sets['altnames'] = [tmp.strip() for tmp in altnametg.contents if isinstance(tmp, bs4.NavigableString)]

		# Scrub incoming markup
		for key in list(data_sets.keys()):
			if isinstance(data_sets[key], list):
				data_sets[key] = [bleach.clean(val, tags=[], attributes=[], styles=[], strip=True, strip_comments=True).strip() for val in data_sets[key]]
			else:
				data_sets[key] = bleach.clean(data_sets[key], tags=[], attributes=[], styles=[], strip=True, strip_comments=True).strip()


		if data_sets['yeartg'] and data_sets['yeartg'][0]:
			# print("Non-null data_sets['yeartg']:", data_sets['yeartg'])
			try:
				yearstr = data_sets['yeartg'].pop().split("-")[0]
				tmp_d = datetime.datetime(year=int(yearstr), month=1, day=1)
				data_sets['yeartg'] = calendar.timegm(tmp_d.timetuple())
			except ValueError:
				data_sets['yeartg'] = None
		else:
			data_sets['yeartg'] = None

		# {
		# 	'coostatustg': ['3 Volumes (Ongoing)', '5 Web Volumes (Ongoing)'],
		# 	'orig_pub_tg': ['Media Factory'],
		# 	'eng_pub_tg': [],
		# 	'typetg': ['Web Novel'],
		# 	'genretg': ['Action', 'Adventure', 'Comedy', 'Ecchi', 'Fantasy', 'Romance', 'Seinen'],
		# 	'licensedtg': ['No'],
		# 	'altnames': ['Sendai Yuusha wa Inkyoshitai', 'The Previous Hero wants to Retire', '先代勇者は隠居したい'],
		# 	'authortg': ['Iida K'],
		# 	'artisttg': ['Shimotsuki Eito'],
		# 	'title': 'Sendai Yuusha wa Inkyou Shitai',
		# 	'description': '<p>\n  Three years ago, in the land of Reinbulk, a Legendary Hero was summoned in the Kindom of Leezalion and he succeeded in repelling the Demon King. Now, five students are summoned back into Reinbulk by the Kingdom of Luxeria to fight against the Demon King and the demon army. Unlike the other heroes, Yashiro Yuu has no magical affinity and the Luxeria Kingdom has no intention on acknowledging his existence or returning him to his world.\n </p>\n <p>\n  However, Yuu is actually the previous Hero that had fought the Demon King. Moreover, he is perplexed at the situation since he knows the Demon King has not returned since he sealed him. If the seal was ever broken then he would be automatically summoned instead of normal summoned. Since he already saved the world once and the Demon King hasn’t been unsealed, Yuu decides to leave the demons to the new heroes and retire from the Hero business. So he decides to become an adventurer.\n </p>',
		# 	'tagstg': ['Elves', 'Heroes', 'Magic', 'Monsters', 'Multiple Narrators', 'Protagonist Strong from the Start', 'Strong Male Lead', 'Sword and Sorcery', 'Transported to Another World'],
		# 	'langtg': ['Japanese'],
		# 	'yeartg': ['2013']

		# 	'transcompletetg': ['No'],
		# }

		data_sets['description'] = bleach.clean(descrtg.prettify(), tags=['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol', 'strong', 'ul', 'p'], strip=True).strip()

		series_message = {
			'update_only'   : False,
			'sourcesite'    : "NovelUpdates",
			'title'         : data_sets['title'],
			'alt_titles'    : data_sets['altnames'] + [data_sets['title'], ],

			'desc'          : data_sets['description'],
			# 'homepage'      : data_sets[''],
			'author'        : data_sets['authortg'],
			'illust'        : data_sets['artisttg'],

			'pubdate'       : data_sets['yeartg'],
			'pubnames'      : data_sets['orig_pub_tg'] + data_sets['eng_pub_tg'],
			# 'sourcesite'    : data_sets[''],
			'tags'          : data_sets['tagstg'],

			# AFICT, NovelUpdates doesn't have any english items, but wth.
			'tl_type'       : "translated" if 'English' not in data_sets['langtg'] else "oel",

			# New:
			'coostate'      : "<br />".join(data_sets['coostatustg']),
			'type'          : data_sets['typetg'],
			'genres'        : data_sets['genretg'],
			'licensed'      : "<br />".join(data_sets['licensedtg']),
			'transcomplete' : "<br />".join(data_sets['transcompletetg']),

			'create_tags'   : True,
		}
		# pprint.pprint(series_message)
		series_info_packet = msgpackers.createSeriesInfoPacket(series_message, matchAuthor=True, beta=self.is_beta)
		# print(series_info_packet)

		extra = {}
		extra['tags']     = data_sets['tagstg']
		# extra['homepage'] = seriesPageUrl
		extra['sourcesite']  = 'Unknown'


		chapter_tbl = soup.find("table", id='myTable')
		if not chapter_tbl:
			self.log.error("No chapter table!")
			return

		releases = chapter_tbl.find_all("tr")


		masked_classes = self.getMaskedClasses(soup)


		valid_releases = 0
		for release in releases:
			items = release.find_all("td")
			if len(items) != 3:
				continue

			date_tg, group_tg, chp_tg = items

			rel = datetime.datetime.strptime(date_tg.get_text().strip(), '%m/%d/%y')
			if rel.date() == datetime.date.today():
				reldate = datetime.datetime.now()
			else:
				reldate = datetime.datetime.fromtimestamp(calendar.timegm(rel.timetuple()))

			release_info  = chp_tg.get_text().strip()
			group_name = group_tg.get_text().strip()
			group_name = msgpackers.fixSmartQuotes(group_name)

			linkas = release.find_all('a', class_='chp-release')

			for link in linkas:
				bad = any([tmp in masked_classes for tmp in link['class']])
				if not bad:
					linkfq = link['href']
					if linkfq.startswith("//"):
						linkfq = "https:"+linkfq

					changed = upsertNuItem(self.raw_cur,
						{
							'seriesname'       : title,
							'releaseinfo'      : release_info,
							'groupinfo'        : group_name,
							'referrer'         : seriesPageUrl,
							'outbound_wrapper' : linkfq,
							'release_date'     : reldate,
							'first_seen'       : datetime.datetime.min,
						})
					self.log.info("Upserting outbound wrapper url %s, changed %s rows.", linkfq, changed)

					if changed:
						self.mon_con.incr('new-urls', 1)

			valid_releases += 1

		self.log.info("Found %s releases on page!", valid_releases)
		self.log.info("Committing!")
		self.raw_cur.execute("COMMIT;")
		self.log.info("Committed!")

		# Do not add series without 3 chapters.
		# if valid_releases < 3:
		# 	self.log.warning("Less then three chapters!")
		# 	return

		self.amqp_put_item(series_info_packet)
		return


	def processPage(self, url, content):

		soup = common.util.WebRequest.as_soup(self.content)
		self.extractSeriesReleases(self.pageUrl, soup)




##################################################################################################################################
##################################################################################################################################
##################################################################################################################################



	def extractContent(self):
		# print("Call to extract!")
		# print(self.amqpint)

		self.processPage(self.pageUrl, self.content)


def testJobFromUrl(url):
	import datetime
	import WebMirror.database
	return WebMirror.database.WebPages(
				state     = 'fetching',
				url       = url,
				starturl  = url,
				netloc    = "wat",
				distance  = WebMirror.database.MAX_DISTANCE-2,
				is_text   = True,
				priority  = WebMirror.database.DB_REALTIME_PRIORITY,
				type      = "unknown",
				fetchtime = datetime.datetime.now(),
				)



def test():
	print("Test mode!")
	import logSetup
	import WebMirror.rules
	import WebMirror.Engine
	import WebMirror.Runner
	import multiprocessing
	logSetup.initLogging()

	crawler = WebMirror.Runner.Crawler()
	crawler.start_aggregator()


	c_lok = cookie_lock = multiprocessing.Lock()
	engine = WebMirror.Engine.SiteArchiver(cookie_lock=c_lok, response_queue=crawler.agg_queue)



	engine.dispatchRequest(testJobFromUrl('http://www.novelupdates.com/series/sendai-yuusha-wa-inkyou-shitai'))
	engine.dispatchRequest(testJobFromUrl('http://www.novelupdates.com/series/when-he-comes-close-your-eyes'))
	engine.dispatchRequest(testJobFromUrl('http://www.novelupdates.com/series/kenkyo-kenjitsu-o-motto-ni-ikite-orimasu'))
	engine.dispatchRequest(testJobFromUrl('http://www.novelupdates.com/series/night-ranger/'))
	engine.dispatchRequest(testJobFromUrl('http://www.novelupdates.com/series/mythical-tyrant/'))
	engine.dispatchRequest(testJobFromUrl('http://www.novelupdates.com/series/kenkyo-kenjitsu-o-motto-ni-ikite-orimasu/'))


	crawler.join_aggregator()

if __name__ == "__main__":
	test()

