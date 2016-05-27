


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




class NUSeriesUpdateFilter(WebMirror.OutputFilters.FilterBase.FilterBase):


	wanted_mimetypes = [

							'text/html',
						]
	want_priority    = 50

	loggerPath = "Main.Filter.NovelUpdates.Series"

	# This plugin doesn't need AMQP connectivity at all.
	_needs_amqp = False

	@staticmethod
	def wantsUrl(url):
		want = [
			r'https?://www\.novelupdates\.com/?$',
			r'https?://www\.novelupdates\.com/\?pg=\d+$',
		]
		if any([re.match(pattern, url) for pattern in want]):
			return True
		return False

	def __init__(self, **kwargs):

		self.kwargs     = kwargs


		self.pageUrl    = kwargs['pageUrl']

		self.content    = kwargs['pgContent']
		self.type       = kwargs['type']
		self.db_sess    = kwargs['db_sess']

		self.log.info("Processing NovelUpdates Item")
		super().__init__(**kwargs)


##################################################################################################################################
##################################################################################################################################
##################################################################################################################################


	def extractSeriesReleases(self, seriesPageUrl, soup):

		container = soup.find('div', class_='l-content')
		# print("container: ", container)

		release_tables = container.find_all('table', class_='tablesorter')

		# print("Release tables:", release_tables)

		urls = []
		for table_div in release_tables:
			for item in table_div.find_all("tr"):
				tds = item.find_all('td')
				if len(tds) == 3:
					titled, dummy_released, dummy_groupd = tds
					urls.append(titled.a['href'])

		return set(urls)




	def retrigger_pages(self, releases):
		self.log.info("Total releases found on page: %s. Forcing retrigger of item pages.", len(releases))

		for release_url in releases:
			while 1:
				try:
					have = self.db_sess.query(db.WebPages) \
						.filter(db.WebPages.url == release_url)   \
						.scalar()

					# If we don't have the page, ignore
					# it as the normal new-link upsert mechanism
					# will add it.
					if not have:
						self.log.info("New: '%s'", release_url)

						new = db.WebPages(
								url             = release_url,
								starturl        = "https://www.novelupdates.com/",
								netloc          = 'www.novelupdates.com',
								distance        = 0,
								is_text         = True,
								priority        = db.DB_HIGH_PRIORITY,
								state           = "new",
								addtime         = datetime.datetime.now(),

								# Don't retrigger unless the ignore time has elaped.
								ignoreuntiltime = datetime.datetime.now() - datetime.timedelta(days=1)
							)
						self.db_sess.add(new)
						self.db_sess.commit()



					else:
						# Also, don't reset if it's in-progress
						if have.state in ['fetching', 'processing', 'error', 'removed', 'disabled', 'specialty_deferred', 'specialty_ready'] and have.distance < 1000000:
							self.log.info("Skipping: '%s' (%s, %s, %s)", release_url, have.state, have.distance, have.priority)
							break

						have.distance        = 0
						have.priority        = db.DB_HIGH_PRIORITY
						have.ignoreuntiltime = datetime.datetime.now() - datetime.timedelta(days=1)
						self.log.info("Retriggering page '%s'", release_url)
						have.state = 'new'
						self.db_sess.commit()
						break


				except sqlalchemy.exc.InvalidRequestError:
					print("InvalidRequest error!")
					self.db_sess.rollback()
					traceback.print_exc()
				except sqlalchemy.exc.OperationalError:
					print("InvalidRequest error!")
					self.db_sess.rollback()
				except sqlalchemy.exc.IntegrityError:
					print("[upsertRssItems] -> Integrity error!")
					traceback.print_exc()
					self.db_sess.rollback()





	def processPage(self, url, content):
		soup = WebMirror.util.webFunctions.as_soup(self.content)
		releases = self.extractSeriesReleases(self.pageUrl, soup)
		relcnt = len(releases)
		if relcnt > 0:
			self.log.info("Found %s items to retrigger", relcnt)
		else:
			self.log.error("Found no items to retrigger via NovelUpdates!")
		if releases:
			self.retrigger_pages(releases)




##################################################################################################################################
##################################################################################################################################
##################################################################################################################################



	def extractContent(self):
		# print("Call to extract!")
		# print(self.amqpint)
		self.log.info("NovelUpdates series page filter processing content.")
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

	# engine.dispatchRequest(testJobFromUrl('http://www.novelupdates.com/'))

	for x in range(0, 180):
		engine.dispatchRequest(testJobFromUrl('http://www.novelupdates.com/?pg={num}'.format(num=x)))

	# engine.dispatchRequest(testJobFromUrl('http://www.novelupdates.com/?pg=1'))
	# engine.dispatchRequest(testJobFromUrl('http://www.novelupdates.com/?pg=2'))
	# engine.dispatchRequest(testJobFromUrl('http://www.novelupdates.com/?pg=3'))
	# engine.dispatchRequest(testJobFromUrl('http://www.novelupdates.com/?pg=4'))


if __name__ == "__main__":
	print("Testing")
	test()

