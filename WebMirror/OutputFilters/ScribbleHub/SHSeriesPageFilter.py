





import bs4
import re
import calendar
import datetime
import time
import json
import os.path
import parsedatetime
import bleach

import WebRequest

import common.util.urlFuncs

import WebMirror.OutputFilters.FilterBase
import WebMirror.OutputFilters.util.TitleParsers as titleParsers
import WebMirror.OutputFilters.util.MessageConstructors as msgpackers


from .. import SeriesPageCommon

class SHSeriesPageFilter(WebMirror.OutputFilters.FilterBase.FilterBase):
	wanted_mimetypes = [
							'text/html',
						]
	want_priority    = 55

	loggerPath = "Main.Filter.RoyalRoad.Page"

	match_re = re.compile(r"^https?://(?:www\.)?scribblehub\.com/series/(\d+)(?:/[a-zA-Z0-9-]+/?|/?)?", flags=re.IGNORECASE)

	@classmethod
	def wantsUrl(cls, url):
		if cls.match_re.search(url):
			print("SHSeriesPageFilter Wants url: '%s'" % url)
			return True
		# else:
		# 	print("SHSeriesPageFilter doesn't want url: '%s'" % url)ty

		return False

	def __init__(self, **kwargs):

		self.kwargs     = kwargs


		self.pageUrl    = kwargs['pageUrl']

		self.content    = kwargs['pgContent']
		self.type       = kwargs['type']

		self.log.info("Processing ScribbleHub Series Page")
		super().__init__(**kwargs)


##################################################################################################################################
##################################################################################################################################
##################################################################################################################################


	def extractSeriesReleases(self, seriesPageUrl, soup):


		match = self.match_re.search(seriesPageUrl)
		series_id = match.group(1)

		titletg  = soup.find("div", class_='fic_title')
		authortg = soup.find("span", class_='auth_name_fic')

		if not titletg:
			self.log.error("Could not find title tag!")
			return []

		if not authortg:
			self.log.error("Could not find author tag!")
			return []

		metas = soup.find_all("script", type="application/ld+json")
		agg_meta = {}
		for meta in metas:
			loaded = json.loads(meta.get_text())
			for k, v in loaded.items():
				agg_meta[k] = v

		rating     = float(agg_meta.get('ratingValue', "0"))
		rating_cnt = float(agg_meta.get('ratingCount', "0"))

		self.log.info("Rating value: %s, Rating cnt: %s", rating, rating_cnt)

		if rating < SeriesPageCommon.MIN_RATING_STARS:
			self.log.error("Item rating below upload threshold: %s", rating)
			return []

		if rating_cnt < SeriesPageCommon.MIN_RATE_CNT:
			self.log.error("Item has insufficent ratings: %s", rating_cnt)
			return []

		title  = titletg.get_text().strip()
		author = authortg.get_text().strip()

		title = bleach.clean(title, tags=[], attributes=[], styles=[], strip=True, strip_comments=True)
		author = bleach.clean(author, tags=[], attributes=[], styles=[], strip=True, strip_comments=True)

		descDiv = soup.find('div', class_='wi_fic_desc')
		if not descDiv or not descDiv.p:
			self.log.error("Incomplete or broken description?")
			return []

		desc = []
		for segment in descDiv:
			if isinstance(segment, bs4.NavigableString):
				desc.append(str(segment).strip())
			else:
				if segment.get_text().strip():
					desc.append(segment.get_text().strip())

		desc = ['<p>{}</p>'.format(line) for line in desc if line.strip()]

		tags = []
		tagdiv = soup.find('span', class_='wi_fic_showtags')
		for tag in tagdiv.find_all('a', class_='stag'):
			tagtxt = SeriesPageCommon.clean_tag(tag.get_text())
			tagtxt = SeriesPageCommon.fix_tag(tagtxt)
			tags.append(tagtxt)

		# These are separate on SH, but I'm just treating them as tags.
		for tag in soup.find_all('li', class_='mature_contains'):
			tagtxt = SeriesPageCommon.clean_tag(tag.get_text())
			tagtxt = SeriesPageCommon.fix_tag(tagtxt)
			tags.append(tagtxt)

		genres = []
		genrediv = soup.find('span', class_='wi_fic_genre')
		for genre in genrediv.find_all('a', class_='fic_genre'):
			genretxt = SeriesPageCommon.clean_tag(genre.get_text())
			genretxt = SeriesPageCommon.fix_genre(genretxt)
			genres.append(genretxt)


		seriesmeta = {}

		seriesmeta['title']       = msgpackers.fix_string(title)
		seriesmeta['author']      = msgpackers.fix_string(author)
		seriesmeta['tags']        = tags
		seriesmeta['homepage']    = seriesPageUrl
		seriesmeta['desc']        = "\r\n".join(desc)
		seriesmeta['tl_type']     = 'oel'
		seriesmeta['sourcesite']  = 'ScribbleHub'
		seriesmeta['create_tags'] = True

		meta_pkt = msgpackers.createSeriesInfoPacket(seriesmeta, matchAuthor=True)
		extra = {}
		extra['tags']       = tags
		extra['genres']     = genres
		extra['homepage']   = seriesPageUrl
		extra['sourcesite'] = 'ScribbleHub'


		self.log.info("Found %s tags, %s genres", len(tags), len(genres))

		chapters = soup.find_all("li", class_='toc_w')

		raw_retval = []
		for chapter in chapters:

			cname, cdate = chapter.a, chapter.span

			if not (cname and cdate):
				self.log.warning("Row with invalid number of entries?")
				continue

			if not cdate.get("title"):
				self.log.error("No time entry?")
				continue

			timestr = cdate.get("title").strip()
			itemDate, status = parsedatetime.Calendar().parse(timestr)

			if status < 1:
				self.log.warning("Failure processing date: %s", timestr)
				continue

			reldate = time.mktime(itemDate)

			relurl = common.util.urlFuncs.rebaseUrl(cname['href'], seriesPageUrl)


			chp_title = cname.get_text().strip()
			# print("Chp title: '{}'".format(chp_title))
			vol, chp, frag, _ = titleParsers.extractTitle(chp_title + " " + title)

			raw_item = {}
			raw_item['srcname']   = "ScribbleHub"
			raw_item['published'] = float(reldate)
			raw_item['linkUrl']   = relurl

			raw_msg = msgpackers._buildReleaseMessage(
				raw_item,
				title,
				vol,
				chp,
				frag,
				author      = author,
				postfix     = chp_title,
				tl_type     = 'oel',
				extraData   = extra,
				matchAuthor = True
				)

			# print("Chapter:", raw_item)
			raw_retval.append(raw_msg)

		raw_retval = SeriesPageCommon.check_fix_numbering(self.log, raw_retval, series_id, sh=True)

		# Do not add series without 3 chapters.
		if len(raw_retval) < 3:
			self.log.info("Less then three chapters!")
			return []

		if not raw_retval:
			self.log.info("Retval empty?!")
			return []

		retval = [msgpackers.createReleasePacket(raw_msg) for raw_msg in raw_retval] + [meta_pkt]

		self.log.info("Found %s chapter releases on series page!", len(retval))
		return retval


	def sendReleases(self, releases):
		self.log.info("Total releases found on page: %s. Emitting messages into AMQP local queue.", len(releases))
		self.amqp_put_many(releases)




	def processPage(self, url, content):
		# Ignore 404 chapters
		if "<title> | Scribble Hub</title>" in content:
			self.log.warning("No series?")
			return

		soup = WebRequest.as_soup(self.content)
		releases = self.extractSeriesReleases(self.pageUrl, soup)
		if releases:
			self.sendReleases(releases)
		else:
			self.log.info("No releases found on page?")




##################################################################################################################################
##################################################################################################################################
##################################################################################################################################



	def extractContent(self):
		# print("Call to extract!")
		# print(self.amqpint)

		self.processPage(self.pageUrl, self.content)


def test():
	print("Test mode!")
	import logSetup
	from WebMirror.Engine import SiteArchiver
	import common.database as db

	logSetup.initLogging()

	def fetch(url):
		with db.session_context() as sess:
			archiver = SiteArchiver(
					cookie_lock   = None,
					db_interface  = sess,
					new_job_queue = None
				)
			archiver.synchronousJobRequest(url, ignore_cache=True, debug=True)



	fetch('https://www.scribblehub.com/series/112220/the-dragonkin-and-the-succubus/')
	fetch('https://www.scribblehub.com/series/107977/bookworld-online-marsh-man/')
	fetch('https://www.scribblehub.com/series/100965/reincarnation-of-a-worthless-man/')
	fetch('https://www.scribblehub.com/series/106548/i-am-an-eggplant-bl/')
	fetch('https://www.scribblehub.com/series/81596/the-broken-system-what-bred-a-king/')
	fetch('https://www.scribblehub.com/series/82656/the-th-demon-lord/')
	fetch('https://www.scribblehub.com/series/66899/the-trials-path-toward-godhood-warning-mature-content/')
	fetch('https://www.scribblehub.com/series/106712/lust-knight/')
	fetch('https://www.scribblehub.com/series/111453/the-forgotten-character/')
	fetch('https://www.scribblehub.com/series/69064/morbid/')
	fetch('https://www.scribblehub.com/series/34196/the-legend-of-the-fake-hero/')
	fetch('https://www.scribblehub.com/series/58245/a-reincarnated-demons-tales-of-wonder/')
	fetch('https://www.scribblehub.com/series/86103/the-demon-lords-successor/')
	fetch('https://www.scribblehub.com/series/93826/waking-up-as-a-spaceship-whats-a-ship-girl-supposed-to-do-now/')
	fetch('https://www.scribblehub.com/series/94224/the-man-who-killed-the-first-monster/')
	fetch('https://www.scribblehub.com/series/110849/monster-parade/')
	fetch('https://www.scribblehub.com/series/40636/falling-over/')
	fetch('https://www.scribblehub.com/series/94576/psionic-goddess-and-the-akashic-system/')
	fetch('https://www.scribblehub.com/series/98089/the-creed-of-an-avenger-an-arifureta-fanfic/')
	fetch('https://www.scribblehub.com/series/51635/eh-where-did-my-pen-pen-go/')
	fetch('https://www.scribblehub.com/series/81242/summoned-again/')
	fetch('https://www.scribblehub.com/series/62217/ultimate-fruit/')
	fetch('https://www.scribblehub.com/series/108367/the-queen-of-darkness-does-not-want-to-be-the-villain/')
	fetch('https://www.scribblehub.com/series/101250/reborn-as-batmans-little-brother/')
	fetch('https://www.scribblehub.com/series/10442/world-keeper/')
	fetch('https://www.scribblehub.com/series/83275/nero-my-existence-is-perfect/')



	# engine.dispatchRequest(testJobFromUrl('http://www.ScribbleHub.com/fiction/3021'))
	# engine.dispatchRequest(testJobFromUrl('http://www.ScribbleHub.com/fictions/latest-updates/'))

	# engine.dispatchRequest(testJobFromUrl('http://www.ScribbleHub.com/fictions/best-rated/'))
	# fetch('https://www.scribblehub.com/series-ranking/')
	# fetch('https://www.scribblehub.com/series-ranking/?sort=3&order=1')
	# fetch('https://www.scribblehub.com/latest-series/')



if __name__ == "__main__":
	test()

