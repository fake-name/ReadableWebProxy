


import WebMirror.OutputFilters.FilterBase

import WebMirror.OutputFilters.util.MessageConstructors  as msgpackers
from WebMirror.OutputFilters.util.TitleParsers import extractTitle

import bs4
import re
import calendar
import datetime
import WebRequest
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




class FoxTellerSeriesPageFilter(WebMirror.OutputFilters.FilterBase.FilterBase):

	wanted_mimetypes = [
							'text/html',
						]
	want_priority    = 50

	loggerPath = "Main.Filter.FoxTeller"


	@staticmethod
	def wantsUrl(url):
		if re.search(r"^https://www\.foxteller\.com/releases$", url):
			print("FoxTellerSeriesPageFilter Wants url: '%s'" % url)
			return True
		return False

	def __init__(self, **kwargs):

		self.kwargs     = kwargs


		self.pageUrl    = kwargs['pageUrl']

		self.content    = kwargs['pgContent']
		self.type       = kwargs['type']

		self.log.info("Processing FoxTeller Item")

		if "dosuper" in kwargs:
			dosuper = kwargs['dosuper']
		else:
			dosuper = True


		if dosuper:
			super().__init__(**kwargs)


##################################################################################################################################
##################################################################################################################################
##################################################################################################################################


	def extractSeriesReleases(self, row):

		tds = row.find_all("td")
		if len(tds) != 4:
			self.log.warning("Row does not have four <td> tags! Don't know how to handle")
			pdtag = row.prettify()
			for line in pdtag.split("\n"):
				self.log.warning(line)

			return None
		title_td, ch_td, trans_td, release_td = tds



		title  = title_td.find("div", class_='ellipsis-1').get_text(strip=True)

		author = trans_td.get_text(strip=True)


		if not title:
			return None
		if not author:
			return None


		# Cripes this is probably brittle
		series_type = "translated" if "," in author else "oel"

		reldate = float(release_td.span['data-timestamp'])

		chp_title = ch_td.get_text(strip=True)

		vol, chp, frag, _ = extractTitle(chp_title)

		raw_item = {}
		raw_item['srcname']   = 'FoxTeller'
		raw_item['published'] = reldate
		raw_item['linkUrl']   = urllib.parse.urljoin("https://www.foxteller.com", ch_td.a['href'])


		raw_msg = msgpackers._buildReleaseMessage(
							raw_item    = raw_item,
							series      = title,
							vol         = vol,
							chap        = chp,
							frag        = frag,
							# author      = author,
							postfix     = chp_title,
							tl_type     = series_type,
							# matchAuthor = True,
							# looseMatch  = True
						)

		msg     = msgpackers.createReleasePacket(raw_msg)

		return msg


	def sendReleases(self, releases):
		self.log.info("Total releases found on page: %s", len(releases))
		for pkt in releases:
			self.amqp_put_item(pkt)


	def processPage(self, content):

		soup = WebRequest.as_soup(self.content)

		table = soup.find("table", class_='table-latest-releases')
		if table:
			releases = []
			for chunk in table.find_all("tr"):
				try:
					rel = self.extractSeriesReleases(chunk)
					if rel:
						releases.append(rel)


				except Exception:
					traceback.print_exc()

			if releases:
				self.sendReleases(releases)



##################################################################################################################################
##################################################################################################################################
##################################################################################################################################



	def extractContent(self):
		# print("Call to extract!")
		# print(self.amqpint)

		self.processPage(self.content)




def test():
	print("Test mode!")
	import logSetup
	import WebMirror.rules
	import WebMirror.Engine
	import multiprocessing
	logSetup.initLogging()

	c_lok = cookie_lock = multiprocessing.Lock()
	engine = WebMirror.Engine.SiteArchiver(cookie_lock=c_lok)
	engine.dispatchRequest(testJobFromUrl('https://www.foxteller.com/releases'))


	# import WebRequest as webfunc

	# wg = webfunc.WebGetRobust()
	# proc = FoxTellerSeriesPageFilter(pageUrl="urlllllll", pgContent="watttt", type='lolertype', dosuper=False)

	# urls = [
	# 	'https://www.foxteller.com/releases',
	# 	]
	# for url in urls:
	# 	ctnt = wg.getpage(url)
	# 	proc.content = ctnt
	# 	proc.processPage(ctnt)

if __name__ == "__main__":
	test()

