



import bs4
import re
import calendar
import datetime
import time
import json
import os.path
import parsedatetime
import bleach

import WebRequest

import common.util.urlFuncs

import WebMirror.OutputFilters.FilterBase
import WebMirror.OutputFilters.util.TitleParsers as titleParsers
import WebMirror.OutputFilters.util.MessageConstructors as msgpackers


from .. import SeriesPageCommon

class RRLSeriesPageFilter(WebMirror.OutputFilters.FilterBase.FilterBase):
	wanted_mimetypes = [
							'text/html',
						]
	want_priority    = 55

	loggerPath = "Main.Filter.RoyalRoad.Page"

	match_re = re.compile(r"^https?://(?:www\.)?royalroadl?\.com/fiction/(\d+)(?:/?$|/[a-zA-Z0-9\-]+/?$)", flags=re.IGNORECASE)

	@classmethod
	def wantsUrl(cls, url):
		if cls.match_re.search(url):
			print("RRLSeriesPageFilter Wants url: '%s'" % url)
			return True
		# else:
		# 	print("RRLSeriesPageFilter doesn't want url: '%s'" % url)

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

		match = self.match_re.search(seriesPageUrl)
		series_id = match.group(1)



		header   = soup.find("div", class_='fic-title')
		if not header:
			self.log.warning("Series page %s contains no releases. Is this series removed?", seriesPageUrl)
			return []

		titletg  = header.find("h1")
		authortg = header.find("h4")
		authortg.find("span").decompose()

		rating_val   = soup.find("meta", property='books:rating:value')
		rating_scale = soup.find("meta", property='books:rating:scale')


		if not rating_val or not rating_scale:
			return []

		rval_f   = float(rating_val.get('content', "0"))
		rscale_f = float(rating_scale.get('content', "999999"))

		rating = 5 * (rval_f / rscale_f)


		if rating < SeriesPageCommon.MIN_RATING_STARS:
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
				desc.append(str(segment).strip())
			else:
				if segment.get_text().strip():
					desc.append(segment.get_text().strip())

		desc = ['<p>{}</p>'.format(line) for line in desc if line.strip()]

		tags = []
		tagdiv = soup.find('span', class_='tags')
		for tag in tagdiv.find_all('span', class_='label'):
			tagtxt = tag.get_text().strip().lower().replace(" ", "-")
			tagtxt = SeriesPageCommon.fix_tag(tagtxt)
			tags.append(tagtxt)

		info_div = soup.find("div", class_='fiction-info')
		warning_div = info_div.find("div", class_='font-red-sunglo')
		if warning_div:
			for warning_tag in warning_div.find_all('li'):
				tagtxt = warning_tag.get_text().strip().lower().replace(" ", "-")
				tagtxt = SeriesPageCommon.fix_tag(tagtxt)
				tags.append(tagtxt)


		seriesmeta = {}

		seriesmeta['title']       = msgpackers.fix_string(title)
		seriesmeta['author']      = msgpackers.fix_string(author)
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

			if not cdate.time:
				self.log.error("No time entry?")
				continue

			timestr = cdate.time.get("title").strip()
			itemDate, status = parsedatetime.Calendar().parse(timestr)

			if status < 1:
				self.log.warning("Failure processing date: %s", timestr)
				continue

			reldate = time.mktime(itemDate)

			relurl = common.util.urlFuncs.rebaseUrl(cname.a['href'], seriesPageUrl)


			chp_title = cname.get_text().strip()
			vol, chp, frag, _ = titleParsers.extractTitle(chp_title + " " + title)

			raw_item = {}
			raw_item['srcname']   = "RoyalRoadL"
			raw_item['published'] = float(reldate)
			raw_item['linkUrl']   = relurl

			raw_msg = msgpackers._buildReleaseMessage(
				raw_item,
				title,
				vol,
				chp,
				frag,
				author      = author,
				postfix     = chp_title,
				tl_type     = 'oel',
				extraData   = extra,
				matchAuthor = True
				)

			raw_retval.append(raw_msg)


		raw_retval = SeriesPageCommon.check_fix_numbering(self.log, raw_retval, series_id, rrl=True)

		# Do not add series without 3 chapters.
		if len(raw_retval) < 3:
			self.log.info("Less then three chapters!")
			return []

		if not raw_retval:
			self.log.info("Retval empty?!")
			return []

		retval = [msgpackers.createReleasePacket(raw_msg) for raw_msg in raw_retval] + [meta_pkt]

		self.log.info("Found %s chapter releases on series page!", len(retval))
		return retval


	def sendReleases(self, releases):
		self.log.info("Total releases found on page: %s. Emitting messages into AMQP local queue.", len(releases))
		self.amqp_put_many(releases)




	def processPage(self, url, content):
		# Ignore 404 chapters
		if "<title>Not Found | RoyalRoadL</title>" in content:
			return

		soup = WebRequest.as_soup(self.content)
		releases = self.extractSeriesReleases(self.pageUrl, soup)
		if releases:
			self.sendReleases(releases)




##################################################################################################################################
##################################################################################################################################
##################################################################################################################################



	def extractContent(self):

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

