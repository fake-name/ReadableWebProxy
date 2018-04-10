


import runStatus
runStatus.preloadDicts = False

import WebMirror.OutputFilters.FilterBase

import common.database as db

import WebMirror.OutputFilters.util.MessageConstructors  as msgpackers
from WebMirror.OutputFilters.util.TitleParsers import extractTitle

import bs4
import re
import calendar
import traceback
import datetime
import time
import json
import WebRequest
import common.util.urlFuncs
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




class RRLJsonXmlSeriesUpdateFilter(WebMirror.OutputFilters.FilterBase.FilterBase):


	wanted_mimetypes = [
							'application/xml',
							'application/json',
						]
	want_priority    = 50

	loggerPath = "Main.Filter.RoyalRoad.XmlJsonSeries"


	@staticmethod
	def wantsUrl(url):
		want = set([
			'https://royalroadl.com/api/',
			'http://royalroadl.com/api/',
			'https://www.royalroadl.com/api/',
			'http://www.royalroadl.com/api/',
		])
		url = url.lower()
		if any([url.startswith(tmp) for tmp in want]):

			print("RRLJsonXmlSeriesUpdateFilter Wants url: '%s'" % url)
			return True
		# print("RRLJsonXmlSeriesUpdateFilter doesn't want url: '%s'" % url)
		return False

	def __init__(self, **kwargs):

		self.kwargs     = kwargs


		self.pageUrl    = kwargs['pageUrl']

		self.content    = kwargs['pgContent']
		self.type       = kwargs['type']
		self.db_sess    = kwargs['db_sess']

		self.log.info("Processing RoyalRoadL Json/XML Item")
		super().__init__(**kwargs)


##################################################################################################################################
##################################################################################################################################
##################################################################################################################################


	def extractSeriesReleases(self, seriesPageUrl, soup):

		containers = soup.find_all('div', class_='fiction-list-item')
		# print(soup)
		# print("container: ", containers)
		if not containers:
			return []
		urls = []
		for item in containers:
			div = item.find('h2', class_='fiction-title')
			a = div.find("a")
			if a:
				url = common.util.urlFuncs.rebaseUrl(a['href'], seriesPageUrl)
				urls.append(url)
			else:
				self.log.error("No series in container: %s", item)

		return set(urls)


	def retrigger_pages(self, releases):
		self.log.info("Total releases found on page: %s. Forcing retrigger of item pages.", len(releases))

		for release_url in releases:
			self.retrigger_page(release_url)



	def processPage(self, url, content):
		print("processPage() call")
		# soup = WebRequest.as_soup(self.content)
		# releases = self.extractSeriesReleases(self.pageUrl, soup)
		# if releases:
		# 	self.retrigger_pages(releases)


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
	import settings
	from WebMirror.Engine import SiteArchiver

	logSetup.initLogging()


	urls = [
			'https://royalroadl.com/api/fiction/updates?apiKey=' + settings.RRL_API_KEY,
			# 'https://royalroadl.com/api/fiction/newreleases?apiKey=' + settings.RRL_API_KEY,
	]

	for url in urls:
		with db.session_context() as sess:
			archiver = SiteArchiver(None, sess, None)
			archiver.synchronousJobRequest(url, ignore_cache=True)




if __name__ == "__main__":
	test()


