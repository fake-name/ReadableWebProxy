


import runStatus
runStatus.preloadDicts = False

import WebMirror.OutputFilters.FilterBase

import WebMirror.database as db

import WebMirror.OutputFilters.util.MessageConstructors  as msgpackers
from WebMirror.OutputFilters.util.TitleParsers import extractTitle

import bs4
import re
import calendar
import sqlalchemy.exc
import traceback
import datetime
import time
import json
import WebMirror.util.webFunctions

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




class RRLSeriesUpdateFilter(WebMirror.OutputFilters.FilterBase.FilterBase):


	wanted_mimetypes = [

							'text/html',
						]
	want_priority    = 50

	loggerPath = "Main.Filter.RoyalRoad.Series"


	@staticmethod
	def wantsUrl(url):
		want = [
			'http://www.royalroadl.com/fictions/best-rated/',
			'http://www.royalroadl.com/fictions/latest-updates/',
			'http://www.royalroadl.com/fictions/active-top-50/',
			'http://www.royalroadl.com/fictions/weekly-views-top-50/',
			'http://www.royalroadl.com/fictions/newest/',
			'http://royalroadl.com/fictions/best-rated/',
			'http://royalroadl.com/fictions/latest-updates/',
			'http://royalroadl.com/fictions/active-top-50/',
			'http://royalroadl.com/fictions/weekly-views-top-50/',
			'http://royalroadl.com/fictions/newest/',
		]

		if url in want:

			print("RRLSeriesUpdateFilter Wants url: '%s'" % url)
			return True
		# print("RRLSeriesUpdateFilter doesn't want url: '%s'" % url)
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

		container = soup.find('div', class_='fiction-list-wrapper')
		# print("container: ", container)

		urls = []
		for item in container.find_all("li", class_='fiction'):
			url = item.find('a', text='Fiction Page')['href']
			urls.append(url)

		return set(urls)




	def retrigger_pages(self, releases):
		self.log.info("Total releases found on page: %s. Forcing retrigger of item pages.", len(releases))
		session = db.get_session()
		for release_url in releases:
			while 1:
				try:
					have = session.query(db.WebPages) \
						.filter(db.WebPages.url == release_url)   \
						.scalar()

					# If we don't have the page, ignore
					# it as the normal new-link upsert mechanism
					# will add it.
					if not have:
						self.log.info("New: '%s'", release_url)
						break

					# Also, don't reset if it's in-progress
					if have.state in ['new', 'fetching', 'processing', 'removed']:
						self.log.info("Skipping: '%s' (%s)", release_url, have.state)
						break

					self.log.info("Retriggering page '%s'", release_url)
					have.state = 'new'
					session.commit()
					break


				except sqlalchemy.exc.InvalidRequestError:
					print("InvalidRequest error!")
					session.rollback()
					traceback.print_exc()
				except sqlalchemy.exc.OperationalError:
					print("InvalidRequest error!")
					session.rollback()
				except sqlalchemy.exc.IntegrityError:
					print("[upsertRssItems] -> Integrity error!")
					traceback.print_exc()
					session.rollback()





	def processPage(self, url, content):
		# print("processPage() call")
		soup = WebMirror.util.webFunctions.as_soup(self.content)
		releases = self.extractSeriesReleases(self.pageUrl, soup)
		if releases:
			self.retrigger_pages(releases)




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





	# engine.dispatchRequest(testJobFromUrl('http://www.royalroadl.com/fiction/3021'))
	# engine.dispatchRequest(testJobFromUrl('http://www.royalroadl.com/fictions/latest-updates/'))

	# engine.dispatchRequest(testJobFromUrl('http://www.royalroadl.com/fictions/best-rated/'))
	engine.dispatchRequest(testJobFromUrl('http://www.royalroadl.com/fictions/latest-updates/'))
	engine.dispatchRequest(testJobFromUrl('http://www.royalroadl.com/fictions/active-top-50/'))
	engine.dispatchRequest(testJobFromUrl('http://www.royalroadl.com/fictions/weekly-views-top-50/'))
	engine.dispatchRequest(testJobFromUrl('http://www.royalroadl.com/fictions/newest/'))



if __name__ == "__main__":
	test()

