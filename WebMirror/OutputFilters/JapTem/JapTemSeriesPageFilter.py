


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




class JapTemSeriesPageProcessor(WebMirror.OutputFilters.FilterBase.FilterBase):


	wanted_mimetypes = [

							'text/html',
						]
	want_priority    = 50

	loggerPath = "Main.Filter.JapTem"


	@staticmethod
	def wantsUrl(url):
		if re.search(r"^http://japtem.com/fanfic.php$", url):
			print("JapTemSeriesPageProcessor Wants url: '%s'" % url)
			return True
		return False

	def __init__(self, **kwargs):

		self.kwargs     = kwargs


		self.pageUrl    = kwargs['pageUrl']

		self.content    = kwargs['pgContent']
		self.type       = kwargs['type']

		self.log.info("Processing RSS Item")

		if "dosuper" in kwargs:
			dosuper = kwargs['dosuper']
		else:
			dosuper = True


		if dosuper:
			super().__init__(**kwargs)


##################################################################################################################################
##################################################################################################################################
##################################################################################################################################


	def extractSeriesReleases(self, seriesPageUrl, soup):
		title  = soup.find("div", class_='fanfic_title_div').get_text()
		author = soup.find("div", class_='fanfic_author_div').get_text()
		ratingtg = soup.find("div", class_='fanfic_title_wrapper')
		ratingtg = [item for item in ratingtg.contents if "Rating" in str(item)]
		if not ratingtg:
			ratingtg = ''
		else:
			ratingtg = ratingtg.pop()


		rating, views, chapters = ratingtg.split("·")

		# I think the japtem rating system is just plain out broken.
		if not "no rating" in ratingtg.lower():
			rating_score = float(rating.split()[-1])
			if not rating_score >= MIN_RATING:
				return []


		chapter_num = float(chapters.split()[0])
		if chapter_num < 3:
			return []



		if not title:
			return []
		if not author:
			return []


		descDiv = soup.find('div', class_='fanfic_synopsis')

		if not descDiv:
			print(soup)

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
		seriesmeta['homepage']    = ''
		seriesmeta['desc']        = " ".join([str(para) for para in desc])
		seriesmeta['tl_type']     = 'oel'
		seriesmeta['sourcesite']  = 'JapTem'


		meta_pkt = msgpackers.sendSeriesInfoPacket(seriesmeta)

		extra = {}
		extra['tags']     = tags
		extra['homepage'] = ''
		extra['sourcesite']  = 'JapTem'

		retval = []

		chapters = soup.find("ul", class_='fanfic_chapter_list')
		volumes = chapters.find_all('li', class_='fanfic_volume')
		for volume in volumes:
			releases = volume.find_all('li', class_='fanfic_chapter')
			for release in releases:
				chp_title = release.find("a")

				vol_str = volume.find('div', class_='fanfic_volume_title').get_text()
				reldate = time.time()

				chp_title = chp_title.get_text()

				agg_title = " ".join((vol_str, chp_title))
				# print("Chp title: '{}'".format(chp_title))
				vol, chp, frag, post = extractTitle(agg_title)
				raw_item = {}
				raw_item['srcname']   = "JapTem"
				raw_item['published'] = reldate
				releaseurl = urllib.parse.urljoin(seriesPageUrl, release.a['href'])
				raw_item['linkUrl']   = releaseurl

				msg = msgpackers.buildReleaseMessage(raw_item, title, vol, chp, frag, author=author, postfix=chp_title, tl_type='oel', extraData=extra)
				msg = msgpackers.createReleasePacket(msg)

				retval.append(msg)
		if not retval:
			return []

		retval.append(meta_pkt)
		# return []
		return retval




	def sendReleases(self, releases):
		self.log.info("Total releases found on page: %s", len(releases))
		for pkt in releases:
			self.amqp_put_item(pkt)




	def processPage(self, content):

		soup = bs4.BeautifulSoup(self.content)

		for chunk in soup.find_all('li', class_='fanfic_title'):
			try:
				releases = self.extractSeriesReleases(self.pageUrl, chunk)

				if releases:
					self.sendReleases(releases)
			except Exception:
				traceback.print_exc()





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
	engine.dispatchRequest(testJobFromUrl('http://japtem.com/fanfic.php'))


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

