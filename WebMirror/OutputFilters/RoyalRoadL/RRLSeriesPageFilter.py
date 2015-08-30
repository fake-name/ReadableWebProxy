


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

	loggerPath = "Main.Filter.RoyalRoad"


	@staticmethod
	def wantsUrl(url):
		if re.search(r"^http://www\.royalroadl\.com/fiction/\d+/?$", url):
			print("RRLSeriesPageProcessor Wants url: '%s'" % url)
			return True
		return False

	def __init__(self, **kwargs):

		self.kwargs     = kwargs


		self.pageUrl    = kwargs['pageUrl']

		self.content    = kwargs['pgContent']
		self.type       = kwargs['type']

		self.log.info("Processing RSS Item")
		super().__init__()


##################################################################################################################################
##################################################################################################################################
##################################################################################################################################


	def extractSeriesReleases(self, seriesPageUrl, soup):

		titletg  = soup.find("h1", class_='fiction-title')
		authortg = soup.find("span", class_='author')
		ratingtg = soup.find("span", class_='overall')

		if not ratingtg:
			return []

		if not float(ratingtg['score']) >= MIN_RATING:
			return []

		if not titletg:
			return []
		if not authortg:
			return []
		if not ratingtg:
			return []

		title  = titletg.get_text()
		author = authortg.get_text()
		assert author.startswith("by ")
		author = author[2:].strip()


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

		pkt = msgpackers.sendSeriesInfoPacket(seriesmeta)

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
			vol, chp, frag, post = extractTitle(chp_title)

			raw_item = {}
			raw_item['srcname']   = "RoyalRoadL"
			raw_item['published'] = reldate
			raw_item['linkUrl']   = release.a['href']

			msg = msgpackers.buildReleaseMessage(raw_item, title, vol, chp, frag, author=author, postfix=chp_title, tl_type='oel', extraData=extra)
			retval.append(msg)

		if not retval:
			return []
		self.amqpint.put_item(pkt)
		return retval




	def sendReleases(self, releases):
		self.log.info("Total releases found on page: %s", len(releases))
		for release in releases:
			pkt = msgpackers.createReleasePacket(release)
			self.amqpint.put_item(pkt)




	def processPage(self, url, content):

		soup = bs4.BeautifulSoup(self.content)
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
	import multiprocessing
	logSetup.initLogging()

	c_lok = cookie_lock = multiprocessing.Lock()
	engine = WebMirror.Engine.SiteArchiver(cookie_lock=c_lok)



	engine.dispatchRequest(testJobFromUrl('http://www.royalroadl.com/fiction/3021'))
	# engine.dispatchRequest(testJobFromUrl('http://www.royalroadl.com/fictions/latest-updates'))



if __name__ == "__main__":
	test()

