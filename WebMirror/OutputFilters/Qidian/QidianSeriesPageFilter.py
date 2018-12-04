



import bs4
import re
import calendar
import datetime
import time
import json
import os.path
import parsedatetime
import bleach

import urllib.parse
import WebRequest

import common.util.urlFuncs

import WebMirror.OutputFilters.FilterBase
import WebMirror.OutputFilters.util.TitleParsers as titleParsers
import WebMirror.OutputFilters.util.MessageConstructors as msgpackers

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


def load_lut():
	outf = os.path.join(os.path.split(__file__)[0], 'royal_roadl_overrides.json')
	jctnt = open(outf).read()
	lut = json.loads(jctnt)
	return lut



class QidianSeriesPageFilter(WebMirror.OutputFilters.FilterBase.FilterBase):


	wanted_mimetypes = [
							'text/html',
						]
	want_priority    = 55

	loggerPath = "Main.Filter.QidianWebnovel.Page"



	@staticmethod
	def wantsUrl(url):
		netloc = urllib.parse.urlsplit(url).netloc
		return netloc.lower().endswith(".webnovel.com")

	def __init__(self, **kwargs):

		self.kwargs     = kwargs


		self.pageUrl    = kwargs['pageUrl']

		self.content    = kwargs['pgContent']
		self.type       = kwargs['type']

		self.log.info("Processing Qidian page")
		super().__init__(**kwargs)


##################################################################################################################################
##################################################################################################################################
##################################################################################################################################


	def extractSeriesReleases(self, seriesPageUrl, soup):
		chapter_divs = soup.find_all("a", class_='chapter-link')
		retval = []

		for linka in chapter_divs:
			state   = linka['data-preprocessor-state']
			vol     = linka['data-preprocessor-vol']
			chp     = linka['data-preprocessor-chp']
			name    = linka['data-preprocessor-name']
			index   = linka['data-preprocessor-index']
			title   = linka['data-preprocessor-title']
			reldate = linka['data-preprocessor-reldate']
			href    = linka['href']



			itemDate, status = parsedatetime.Calendar().parse(reldate)

			if status < 1:
				continue

			reldate = time.mktime(itemDate)

			relurl = common.util.urlFuncs.rebaseUrl(linka['href'] + "/", seriesPageUrl)


			print([vol, chp, state, linka])

			raw_item = {}
			raw_item['srcname']   = "Qidian"
			raw_item['published'] = float(reldate)
			raw_item['linkUrl']   = relurl

			if state == '0':
				raw_msg = msgpackers.buildReleaseMessageWithType(raw_item, title, None, index, None, tl_type='translated')
				retval.append(msgpackers.serialize_message(raw_msg))
			elif state == "2":
				raw_msg = msgpackers.buildReleaseDeleteMessageWithType(raw_item, title, None, index, None, tl_type='translated')
				retval.append(msgpackers.serialize_message(raw_msg))
			else:
				print("Unknown state:", state)

		# Do not add series without 3 chapters.
		if len(retval) < 3:
			self.log.info("Less then three chapters!")
			return []

		# if not retval:
		# 	self.log.info("Retval empty?!")
		# 	return []

		# return []

		return retval


	def sendReleases(self, releases):
		self.log.info("Total releases found on page: %s. Emitting messages into AMQP local queue.", len(releases))
		for release in releases:
			self.amqp_put_item(release)


	def check_translated(self, soup):
		detail_div = soup.find("div", class_='det-info')

		strongs = detail_div.find_all("strong")

		if 'Translator:' in [tmp.get_text(strip=True) for tmp in strongs]:
			return True

		return False


	def processPage(self, url_ignored, content):
		# Ignore 404 chapters
		if "<title>Not Found | RoyalRoadL</title>" in content:
			return

		soup = WebRequest.as_soup(self.content)

		if not self.check_translated(soup):
			return

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

