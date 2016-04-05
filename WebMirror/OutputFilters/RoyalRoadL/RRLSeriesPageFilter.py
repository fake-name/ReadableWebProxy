


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




class RRLSeriesPageProcessor(WebMirror.OutputFilters.FilterBase.FilterBase):


	wanted_mimetypes = [

							'text/html',
						]
	want_priority    = 50

	loggerPath = "Main.Filter.RoyalRoad.Page"


	@staticmethod
	def wantsUrl(url):
		if re.search(r"^http://(?:www\.)?royalroadl\.com/fiction/\d+/?$", url):
			print("RRLSeriesPageProcessor Wants url: '%s'" % url)
			return True
		return False

	def __init__(self, **kwargs):

		self.kwargs     = kwargs


		self.pageUrl    = kwargs['pageUrl']

		self.content    = kwargs['pgContent']
		self.type       = kwargs['type']

		self.log.info("Processing RoyalRoadL Item")
		super().__init__(**kwargs)


##################################################################################################################################
##################################################################################################################################
##################################################################################################################################


	def extractSeriesReleases(self, seriesPageUrl, soup):

		titletg  = soup.find("h1", class_='fiction-title')
		authortg = soup.find("span", class_='author')
		ratingtg = soup.find("span", class_='overall')

		if not ratingtg:
			self.log.info("Could not find rating tag!")
			return []


		rating = float(ratingtg['score'])
		if not rating >= MIN_RATING and rating != 0.0:
			self.log.info("Item rating below upload threshold: %s", rating)
			return []

		if not titletg:
			self.log.info("Could not find title tag!")
			return []
		if not authortg:
			self.log.info("Could not find author tag!")
			return []


		title  = titletg.get_text()
		author = authortg.get_text()
		assert author.startswith("by ")
		author = author[2:].strip()


		title = bleach.clean(title, tags=[], attributes=[], styles=[], strip=True, strip_comments=True)
		author = bleach.clean(author, tags=[], attributes=[], styles=[], strip=True, strip_comments=True)

		descDiv = soup.find('div', class_='description')
		paras = descDiv.find_all("p")
		tags = []

		desc = []
		for para, text in [(para, para.get_text()) for para in paras]:
			if text.lower().startswith('categories:'):
				tagstr = text.split(":", 1)[-1]
				items = tagstr.split(",")
				[tags.append(item.strip()) for item in items if item.strip()]
			else:
				desc.append(para)


		seriesmeta = {}

		seriesmeta['title']       = title
		seriesmeta['author']      = author
		seriesmeta['tags']        = tags
		seriesmeta['homepage']    = seriesPageUrl
		seriesmeta['desc']        = " ".join([str(para) for para in desc])
		seriesmeta['tl_type']     = 'oel'
		seriesmeta['sourcesite']  = 'RoyalRoadL'

		pkt = msgpackers.createSeriesInfoPacket(seriesmeta, matchAuthor=True)

		extra = {}
		extra['tags']     = tags
		extra['homepage'] = seriesPageUrl
		extra['sourcesite']  = 'RoyalRoadL'


		chapters = soup.find("div", class_='chapters')
		releases = chapters.find_all('li', class_='chapter')

		retval = []
		for release in releases:
			chp_title, reldatestr = release.find_all("span")
			rel = datetime.datetime.strptime(reldatestr.get_text(), '%d/%m/%y')
			if rel.date() == datetime.date.today():
				reldate = time.time()
			else:
				reldate = calendar.timegm(rel.timetuple())

			chp_title = chp_title.get_text()
			# print("Chp title: '{}'".format(chp_title))
			vol, chp, frag, post = extractTitle(chp_title + " " + title)

			raw_item = {}
			raw_item['srcname']   = "RoyalRoadL"
			raw_item['published'] = reldate
			raw_item['linkUrl']   = release.a['href']

			msg = msgpackers.buildReleaseMessage(raw_item, title, vol, chp, frag, author=author, postfix=chp_title, tl_type='oel', extraData=extra, matchAuthor=True)
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

		# Do not add series without 3 chapters.
		if len(retval) < 3:
			self.log.info("Less then three chapters!")
			return []



		if not retval:
			self.log.info("Retval empty?!")
			return []
		self.amqp_put_item(pkt)
		return retval




	def sendReleases(self, releases):
		self.log.info("Total releases found on page: %s. Emitting messages into AMQP local queue.", len(releases))
		for release in releases:
			pkt = msgpackers.createReleasePacket(release)
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



	engine.dispatchRequest(testJobFromUrl('http://royalroadl.com/fiction/3333'))
	# engine.dispatchRequest(testJobFromUrl('http://www.royalroadl.com/fiction/2850'))
	# engine.dispatchRequest(testJobFromUrl('http://www.royalroadl.com/fictions/latest-updates/'))

	# engine.dispatchRequest(testJobFromUrl('http://www.royalroadl.com/fictions/best-rated/'))
	# engine.dispatchRequest(testJobFromUrl('http://www.royalroadl.com/fictions/latest-updates/'))
	# engine.dispatchRequest(testJobFromUrl('http://www.royalroadl.com/fictions/active-top-50/'))
	# engine.dispatchRequest(testJobFromUrl('http://www.royalroadl.com/fictions/weekly-views-top-50/'))
	# engine.dispatchRequest(testJobFromUrl('http://www.royalroadl.com/fictions/newest/'))

	crawler.join_aggregator()

if __name__ == "__main__":
	test()

