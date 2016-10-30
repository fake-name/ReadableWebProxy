


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
import common.util.webFunctions
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
	want_priority    = 55

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

		header   = soup.find("div", class_='fic-title')
		titletg  = header.find("h2")
		authortg = header.find("h4")
		authortg.find("span").decompose()

		ratingtg_type_1 = soup.find("div", class_='rating')
		ratingtg_type_2 = soup.find("li", text=re.compile('Overall Score'))


		if ratingtg_type_1:
			startg = ratingtg_type_1.find("span", class_='star')
		elif ratingtg_type_2:
			# print(ratingtg_type_2)
			starcontainer = ratingtg_type_2.find_next_sibling("li")
			if not starcontainer:
				self.log.error("Could not find rating tag (starcontainer)!")
				return []
			startg = starcontainer.find("span", class_='star')
			if not startg:
				self.log.error("Could not find rating tag (startg)!")
				return []


		else:
			self.log.error("Could not find rating tag!")
			return []

		ratingcls = [tmp for tmp in startg['class'] if re.match(r"star\-\d+", tmp)]
		rating = ratingcls[0].split("-")[-1]

		rating = float(rating) / 10
		rating = rating * 2  # Normalize to 1-10 scale
		# print(startg['class'])
		if not ratingcls:
			return []

		if not rating >= MIN_RATING and rating != 0.0:
			self.log.error("Item rating below upload threshold: %s", rating)
			return []

		if not titletg:
			self.log.error("Could not find title tag!")
			return []
		if not authortg:
			self.log.error("Could not find author tag!")
			return []


		title  = titletg.get_text().strip()
		author = authortg.get_text().strip()



		title = bleach.clean(title, tags=[], attributes=[], styles=[], strip=True, strip_comments=True)
		author = bleach.clean(author, tags=[], attributes=[], styles=[], strip=True, strip_comments=True)

		descDiv = soup.find('div', class_='description')
		if not descDiv or not descDiv.div:
			self.log.error("Incomplete or broken description?")
			return []

		desc = []
		for segment in descDiv.div:
			if isinstance(segment, bs4.NavigableString):
				# print(("NavigableString", str(segment).strip(), ))
				desc.append(str(segment).strip())
			else:
				if segment.get_text().strip():
					# print(("get_text", segment.get_text().strip(), ))
					desc.append(segment.get_text().strip())

		desc = ['<p>{}</p>'.format(line) for line in desc if line.strip()]
		# print(desc)

		tags = []
		tagdiv = soup.find('div', class_='tags')
		for tag in tagdiv.find_all('span', class_='label'):
			tags.append(tag.get_text().strip())

		seriesmeta = {}

		seriesmeta['title']       = title
		seriesmeta['author']      = author
		seriesmeta['tags']        = tags
		seriesmeta['homepage']    = seriesPageUrl
		seriesmeta['desc']        = "\r\n".join(desc)
		seriesmeta['tl_type']     = 'oel'
		seriesmeta['sourcesite']  = 'RoyalRoadL'
		seriesmeta['create_tags'] = True


		meta_pkt = msgpackers.createSeriesInfoPacket(seriesmeta, matchAuthor=True)
		extra = {}
		extra['tags']     = tags
		extra['homepage'] = seriesPageUrl
		extra['sourcesite']  = 'RoyalRoadL'


		chapters = soup.find_all("tr", attrs={"data-url" : True})

		raw_retval = []
		for chapter in chapters:
			if len(chapter.find_all("td")) != 2:
				self.log.warning("Row with invalid number of entries?")
				continue
			cname, cdate = chapter.find_all("td")

			reldate = cdate.time['unixtime']
			relurl = common.util.urlFuncs.rebaseUrl(cname.a['href'], seriesPageUrl)


			chp_title = cname.get_text().strip()
			# print("Chp title: '{}'".format(chp_title))
			vol, chp, frag, post = extractTitle(chp_title + " " + title)

			raw_item = {}
			raw_item['srcname']   = "RoyalRoadL"
			raw_item['published'] = float(reldate)
			raw_item['linkUrl']   = relurl

			raw_msg = msgpackers.buildReleaseMessage(raw_item, title, vol, chp, frag, author=author, postfix=chp_title, tl_type='oel', extraData=extra, matchAuthor=True)

			raw_retval.append(raw_msg)

		missing_chap = 0
		for item in raw_retval:
			if not (item['vol'] or item['chp']):
				missing_chap += 1

		if len(raw_retval):
			unnumbered = (missing_chap/len(raw_retval)) * 100
			if len(raw_retval) >= 5 and unnumbered > 80:
				self.log.warning("Item seems to not have numbered chapters. Adding simple sequential chapter numbers.")
				chap = 1
				for item in raw_retval:
					item['vol'] = None
					item['chp'] = chap
					chap += 1

		# Do not add series without 3 chapters.
		if len(raw_retval) < 3:
			self.log.info("Less then three chapters!")
			return []

		if not raw_retval:
			self.log.info("Retval empty?!")
			return []

		self.amqp_put_item(meta_pkt)
		retval = [msgpackers.createReleasePacket(raw_msg) for raw_msg in raw_retval]
		return retval


	def sendReleases(self, releases):
		self.log.info("Total releases found on page: %s. Emitting messages into AMQP local queue.", len(releases))
		for release in releases:
			self.amqp_put_item(release)




	def processPage(self, url, content):
		# Ignore 404 chapters
		if "<title>Not Found | RoyalRoadL</title>" in content:
			return

		soup = common.util.webFunctions.as_soup(self.content)
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

