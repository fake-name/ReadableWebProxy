


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




class NUSeriesPageProcessor(WebMirror.OutputFilters.FilterBase.FilterBase):


	wanted_mimetypes = [

							'text/html',
						]
	want_priority    = 50

	loggerPath = "Main.Filter.NoveUpdates.Page"


	@staticmethod
	def wantsUrl(url):
		if re.search(r"^https?://(?:www\.)?novelupdates\.com/series/.+/?$", url):
			print("NUSeriesPageProcessor Wants url: '%s'" % url)
			return True
		return False

	def __init__(self, **kwargs):

		self.kwargs     = kwargs


		self.pageUrl    = kwargs['pageUrl']

		self.content    = kwargs['pgContent']
		self.type       = kwargs['type']

		self.log.info("Processing NovelUpdates series page")
		super().__init__(**kwargs)


##################################################################################################################################
##################################################################################################################################
##################################################################################################################################


	def extractSeriesReleases(self, seriesPageUrl, soup):

		titletg  = soup.find("h4", class_='seriestitle')
		altnametg  = soup.find("div", id='editassociated')
		descrtg  = soup.find("div", id='editdescription')



		link_sets = {
			'authortg'        : soup.find("div", id='showauthors'),
			'artisttg'        : soup.find("div", id='showartists'),
			'langtg'          : soup.find("div", id='showlang'),
			'genretg'         : soup.find("div", id='seriesgenre'),
			'tagstg'          : soup.find("div", id='showtags'),
			'typetg'          : soup.find("div", id='showtype'),
			'orig_pub_tg'     : soup.find("div", id='showopublisher'),
			'eng_pub_tg'      : soup.find("div", id='showepublisher'),
		}

		text_sets = {
			'transcompletetg' : soup.find("div", id='showtranslated'),
			'yeartg'          : soup.find("div", id='edityear'),
			'coostatustg'     : soup.find("div", id='editstatus'),
			'licensedtg'      : soup.find("div", id='showlicensed'),
			}

		if not titletg:
			self.log.warn("Could not find item title!")
			return []
		if not altnametg:
			self.log.warn("Could not find alt-name container tag!")
			return []
		if not descrtg:
			self.log.warn("Could not find description container tag!")
			return []

		data_sets = {}
		for key in list(link_sets.keys()):
			if not link_sets[key]:
				self.log.warn("Could not find tag for name: '%s'", key)
				return []
			data_sets[key] = [tag.get_text() for tag in link_sets[key].find_all("a")]

		for key in list(text_sets.keys()):
			if not text_sets[key]:
				self.log.warn("Could not find tag for name: '%s'", key)
				return []
			data_sets[key] = [tmp.strip() for tmp in text_sets[key].contents if isinstance(tmp, bs4.NavigableString)]

		title  = titletg.get_text().strip()

		data_sets['title'] = title
		data_sets['altnames'] = [tmp.strip() for tmp in altnametg.contents if isinstance(tmp, bs4.NavigableString)]
		data_sets['description'] = bleach.clean(descrtg.prettify(), tags=['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol', 'strong', 'ul', 'p'], strip=True).strip()

		print(title  )
		print(data_sets)

		# Scrub incoming markup
		for key in list(data_sets.keys()):
			data_sets[key] = [bleach.clean(val, tags=[], attributes=[], styles=[], strip=True, strip_comments=True) for val in data_sets[key]]



		return []

		title = bleach.clean(title, tags=[], attributes=[], styles=[], strip=True)

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
		seriesmeta['sourcesite']  = 'Unknown'

		pkt = msgpackers.createSeriesInfoPacket(seriesmeta, matchAuthor=True)

		extra = {}
		extra['tags']     = tags
		extra['homepage'] = seriesPageUrl
		extra['sourcesite']  = 'Unknown'


		chapters = soup.find("div", class_='chapters')
		releases = chapters.find_all('li', class_='chapter')

		# retval = []
		# for release in releases:
		# 	chp_title, reldatestr = release.find_all("span")
		# 	rel = datetime.datetime.strptime(reldatestr.get_text(), '%d/%m/%y')
		# 	if rel.date() == datetime.date.today():
		# 		reldate = time.time()
		# 	else:
		# 		reldate = calendar.timegm(rel.timetuple())

		# 	chp_title = chp_title.get_text()
		# 	# print("Chp title: '{}'".format(chp_title))
		# 	vol, chp, frag, post = extractTitle(chp_title)

		# 	raw_item = {}
		# 	raw_item['srcname']   = "Wattt"
		# 	raw_item['published'] = reldate
		# 	raw_item['linkUrl']   = release.a['href']

		# 	msg = msgpackers.buildReleaseMessage(raw_item, title, vol, chp, frag, author=author, postfix=chp_title, tl_type='oel', extraData=extra, matchAuthor=True)
		# 	retval.append(msg)

		# missing_chap = 0
		# for item in retval:
		# 	if not (item['vol'] or item['chp']):
		# 		missing_chap += 1

		# if len(retval):
		# 	unnumbered = (missing_chap/len(retval)) * 100
		# 	if len(retval) >= 5 and unnumbered > 80:
		# 		self.log.warning("Item seems to not have numbered chapters. Adding simple sequential chapter numbers.")
		# 		chap = 1
		# 		for item in retval:
		# 			item['vol'] = None
		# 			item['chp'] = chap
		# 			chap += 1

		# # Do not add series without 3 chapters.
		# if len(retval) < 3:
		# 	self.log.info("Less then three chapters!")
		# 	return []



		# if not retval:
		# 	self.log.info("Retval empty?!")
		# 	return []
		# self.amqp_put_item(pkt)
		# return retval

		return []



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



	engine.dispatchRequest(testJobFromUrl('http://www.novelupdates.com/series/sendai-yuusha-wa-inkyou-shitai'))
	# engine.dispatchRequest(testJobFromUrl('http://www.novelupdates.com/series/when-he-comes-close-your-eyes'))
	# engine.dispatchRequest(testJobFromUrl('http://www.novelupdates.com/series/kenkyo-kenjitsu-o-motto-ni-ikite-orimasu'))
	# engine.dispatchRequest(testJobFromUrl('http://www.novelupdates.com/series/night-ranger/'))
	# engine.dispatchRequest(testJobFromUrl('http://www.novelupdates.com/series/mythical-tyrant/'))
	# engine.dispatchRequest(testJobFromUrl('http://www.novelupdates.com/series/kenkyo-kenjitsu-o-motto-ni-ikite-orimasu/'))


	crawler.join_aggregator()

if __name__ == "__main__":
	test()

