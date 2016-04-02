


import runStatus
runStatus.preloadDicts = False

import WebMirror.OutputFilters.FilterBase

import WebMirror.OutputFilters.util.MessageConstructors  as msgpackers
from WebMirror.OutputFilters.util.TitleParsers import extractTitle

import bs4
import re
import calendar
import unshortenit
import WebMirror.util.webFunctions
import time
import urllib.parse
import json
import traceback

MIN_RATING = 2.5

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




class BakaTsukiTwitterProcessor(WebMirror.OutputFilters.FilterBase.FilterBase):


	wanted_mimetypes = [

							'text/html',
						]
	want_priority    = 50

	loggerPath = "Main.Filter.BakaTsukiTwitter"


	@staticmethod
	def wantsUrl(url):
		print("WantsURL check: '%s'" % url)
		if url == "https://twitter.com/Baka_Tsuki":
			print("BakaTsukiTwitterProcessor Wants url: '%s'" % url)
			return True
		return False

	def __init__(self, **kwargs):

		self.kwargs     = kwargs


		self.pageUrl    = kwargs['pageUrl']

		self.content    = kwargs['pgContent']
		self.type       = kwargs['type']

		self.log.info("Processing Japtem Item")

		if "dosuper" in kwargs:
			dosuper = kwargs['dosuper']
		else:
			dosuper = True


		if dosuper:
			super().__init__(**kwargs)


##################################################################################################################################
##################################################################################################################################
##################################################################################################################################



	def sendReleases(self, releases):
		self.log.info("Total releases found on page: %s", len(releases))
		for pkt in releases:
			self.amqp_put_item(pkt)


	def processPage(self, content):
		soup = WebMirror.util.webFunctions.as_soup(self.content)

		releases = []
		for tweet in soup.find_all('li', attrs={"data-item-type":"tweet"}):
			if "promoted" in str(tweet['class']):
				continue
			content = tweet.find("p", class_='tweet-text')
			if content and content.a:
				itemtxt = content.get_text()
				titleonly = itemtxt.split("by")[0].split("bY")[0].split("By")[0].split("BY")[0]
				probSeries = titleonly.lower().split("volume")[0].split("chapter")[0].strip()

				itemurl = content.a['data-expanded-url']
				itemurl, status = unshortenit.unshorten(itemurl)
				if status != 200:
					continue
				if not 'http://www.baka-tsuki.org' in itemurl:
					continue

				vol, chp, frag, post = extractTitle(titleonly)

				raw_item = {}
				raw_item['srcname']   = "Baka-Tsuki"
				raw_item['published'] = time.time()
				raw_item['linkUrl']   = itemurl



				msg = msgpackers.buildReleaseMessage(raw_item, probSeries, vol, chp, frag, postfix=post)
				msg = msgpackers.createReleasePacket(msg)
				releases.append(msg)


		self.log.info("Found %s releases from Baka-Tsuki Twitter Feed", len(releases))
		if releases:
			self.sendReleases(releases)


			# try:
			# 	releases = self.extractSeriesReleases(self.pageUrl, chunk)

			# 	if releases:
			# 		self.sendReleases(releases)
			# except Exception:
			# 	traceback.print_exc()





##################################################################################################################################
##################################################################################################################################
##################################################################################################################################



	def extractContent(self):
		# print("Call to extract!")
		# print(self.amqpint)

		self.processPage(self.content)


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
	engine.dispatchRequest(testJobFromUrl('https://twitter.com/Baka_Tsuki'))


	# import WebMirror.util.webFunctions as webfunc

	# wg = webfunc.WebGetRobust()
	# proc = JapTemSeriesPageProcessor(pageUrl="urlllllll", pgContent="watttt", type='lolertype', dosuper=False)

	# urls = [
	# 	'http://japtem.com/fanfic.php',
	# 	]
	# for url in urls:
	# 	ctnt = wg.getpage(url)
	# 	proc.content = ctnt
	# 	proc.processPage(ctnt)

if __name__ == "__main__":
	test()

