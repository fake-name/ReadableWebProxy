


import runStatus
runStatus.preloadDicts = False

import WebMirror.OutputFilters.FilterBase

import WebMirror.OutputFilters.util.MessageConstructors  as msgpackers
from WebMirror.OutputFilters.util.TitleParsers import extractTitle

import bs4
import re
import calendar
import datetime
import time
import json
import WebMirror.util.webFunctions
import bleach
import unshortenit

MIN_RATING = 5

########################################################################################################################
#
#	##     ##    ###    #### ##    ##     ######  ##          ###     ######   ######
#	###   ###   ## ##    ##  ###   ##    ##    ## ##         ## ##   ##    ## ##    ##
#	#### ####  ##   ##   ##  ####  ##    ##       ##        ##   ##  ##       ##
#	## ### ## ##     ##  ##  ## ## ##    ##       ##       ##     ##  ######   ######
#	##     ## #########  ##  ##  ####    ##       ##       #########       ##       ##
#	##     ## ##     ##  ##  ##   ###    ##    ## ##       ##     ## ##    ## ##    ##
#	##     ## ##     ## #### ##    ##     ######  ######## ##     ##  ######   ######
#
########################################################################################################################




class NUSeriesPageProcessor(WebMirror.OutputFilters.FilterBase.FilterBase):


	wanted_mimetypes = [

							'text/html',
						]
	want_priority    = 50

	loggerPath = "Main.Filter.NoveUpdates.Page"


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


##################################################################################################################################
##################################################################################################################################
##################################################################################################################################


	def extractSeriesReleases(self, seriesPageUrl, soup):

		titletg  = soup.find("h4", class_='seriestitle')
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
			print("Non-null data_sets['yeartg']:", data_sets['yeartg'])
			tmp_d = datetime.datetime(year=int(data_sets['yeartg'].pop()), month=1, day=1)
			data_sets['yeartg'] = calendar.timegm(tmp_d.timetuple())
		else:
			data_sets['yeartg'] = None

		{
			# 'coostatustg': ['3 Volumes (Ongoing)', '5 Web Volumes (Ongoing)'],
			# 'orig_pub_tg': ['Media Factory'],
			# 'eng_pub_tg': [],
			# 'typetg': ['Web Novel'],
			# 'genretg': ['Action', 'Adventure', 'Comedy', 'Ecchi', 'Fantasy', 'Romance', 'Seinen'],
			# 'licensedtg': ['No'],
			# 'altnames': ['Sendai Yuusha wa Inkyoshitai', 'The Previous Hero wants to Retire', '先代勇者は隠居したい'],
			# 'authortg': ['Iida K'],
			# 'artisttg': ['Shimotsuki Eito'],
			# 'title': 'Sendai Yuusha wa Inkyou Shitai',
			# 'description': '<p>\n  Three years ago, in the land of Reinbulk, a Legendary Hero was summoned in the Kindom of Leezalion and he succeeded in repelling the Demon King. Now, five students are summoned back into Reinbulk by the Kingdom of Luxeria to fight against the Demon King and the demon army. Unlike the other heroes, Yashiro Yuu has no magical affinity and the Luxeria Kingdom has no intention on acknowledging his existence or returning him to his world.\n </p>\n <p>\n  However, Yuu is actually the previous Hero that had fought the Demon King. Moreover, he is perplexed at the situation since he knows the Demon King has not returned since he sealed him. If the seal was ever broken then he would be automatically summoned instead of normal summoned. Since he already saved the world once and the Demon King hasn’t been unsealed, Yuu decides to leave the demons to the new heroes and retire from the Hero business. So he decides to become an adventurer.\n </p>',
			# 'tagstg': ['Elves', 'Heroes', 'Magic', 'Monsters', 'Multiple Narrators', 'Protagonist Strong from the Start', 'Strong Male Lead', 'Sword and Sorcery', 'Transported to Another World'],
			# 'langtg': ['Japanese'],
			# 'yeartg': ['2013']


			'transcompletetg': ['No'],
		}

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
			'coostate'      : data_sets['coostatustg'],
			'type'          : data_sets['typetg'],
			'genres'        : data_sets['genretg'],
			'licensed'      : data_sets['licensedtg'],
			'transcomplete' : data_sets['transcompletetg'],

		}

		pkt = msgpackers.createSeriesInfoPacket(series_message, matchAuthor=True, beta=self.is_beta)
		# print(pkt)

		extra = {}
		extra['tags']     = data_sets['tagstg']
		# extra['homepage'] = seriesPageUrl
		extra['sourcesite']  = 'Unknown'


		chapter_tbl = soup.find("table", class_='tablesorter')
		releases = chapter_tbl.find_all("tr")

		retval = []
		for release in releases:

			items = release.find_all("td")
			if len(items) == 0:
				continue

			date_tg, group_tg, chp_tg = items

			rel = datetime.datetime.strptime(date_tg.get_text(), '%m/%d/%y')
			if rel.date() == datetime.date.today():
				reldate = time.time()
			else:
				reldate = calendar.timegm(rel.timetuple())

			chp_title  = chp_tg.get_text().strip()
			group_name = group_tg.get_text().strip()
			vol, chp, frag, post = extractTitle(chp_title)

			raw_item = {}
			raw_item['srcname']   = msgpackers.fixSmartQuotes(group_name)
			raw_item['published'] = reldate

			# TODO: This has to move into a preprocessor!
			raw_item['linkUrl'] = self.wg.getHead(chp_tg.a['href'], addlHeaders={"Referer" : seriesPageUrl})

			assert isinstance(raw_item['linkUrl'], str), "novelupdates link not a string?"
			assert not "www.novelupdates.com/extnu/" in raw_item['linkUrl'], "NovelUpdates creepy outbound link thing"

			msg = msgpackers.buildReleaseMessage(raw_item, title, vol, chp, frag, author=data_sets['authortg'], postfix=chp_title, tl_type='translated', extraData=extra, matchAuthor=True)
			retval.append(msg)

		missing_chap = 0
		for item in retval:
			if not (item['vol'] or item['chp']):
				missing_chap += 1

		if len(retval):
			unnumbered = (missing_chap/len(retval)) * 100
			if len(retval) >= 5 and unnumbered > 80:
				self.log.warning("Item seems to not have numbered chapters. Adding simple sequential chapter numbers.")
				chap = 1
				for item in retval:
					item['vol'] = None
					item['chp'] = chap
					chap += 1

		# # Do not add series without 3 chapters.
		# if len(retval) < 3:
		# 	self.log.info("Less then three chapters!")
		# 	return []

		if not retval:
			self.log.info("Retval empty?!")
			return []
		self.amqp_put_item(pkt)
		# return []
		return retval


	def sendReleases(self, releases):
		self.log.info("Total releases found on page: %s. Emitting messages into AMQP local queue.", len(releases))
		for release in releases:
			pkt = msgpackers.createReleasePacket(release, beta=self.is_beta)
			self.amqp_put_item(pkt)




	def processPage(self, url, content):

		soup = WebMirror.util.webFunctions.as_soup(self.content)
		releases = self.extractSeriesReleases(self.pageUrl, soup)
		if releases:
			self.sendReleases(releases)




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

