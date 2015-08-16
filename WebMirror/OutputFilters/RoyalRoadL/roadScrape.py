
#!/usr/bin/python
# from profilehooks import profile

import FeedScrape.RssMonitorDbBase
import TextScrape.utilities.Proxy
import FeedScrape.FeedDataParser
import calendar
import json
import TextScrape.RelinkLookup
import FeedScrape.AmqpInterface
# import TextScrape.RELINKABLE as RELINKABLE
import time
import datetime
# pylint: disable=W0201
#
import TextScrape.HtmlProcessor
import urllib.parse


MIN_RATING = 5

class EmptyFeedError(Exception):
	pass


# buildReleaseMessage(raw_item, series, vol, chap=None, frag=None, postfix='')

class RoyalRoadLMonitor(FeedScrape.RssMonitorDbBase.RssDbBase, FeedScrape.FeedDataParser.DataParser):

	tableName = 'western_monitor'

	loggerPath = 'Main.Rss.RRL'

	# Has to be explicitly overridden, or the inheritnace will
	# asplode.
	log = None
	test_override = []
	htmlProcClass = TextScrape.HtmlProcessor.HtmlPageProcessor


	# All english content
	# Can't filter out poetry at this point, unfortunately (arrrgh)
	root = 'http://www.royalroadl.com/'
	base = [
			'http://www.royalroadl.com/fictions/best-rated/',
			'http://www.royalroadl.com/fictions/latest-updates/',
			'http://www.royalroadl.com/fictions/newest/'
		]


	def __init__(self):
		super().__init__()

		self.dbFunc = TextScrape.utilities.Proxy.EmptyProxy(tableKey='fictionpress', tableName='book_western_items', scanned=[self.root])
		if not hasattr(self, 'wg'):
			import webFunctions
			self.wg = webFunctions.WebGetRobust(logPath='Main.Text.Feed.Web')


	def patchUrl(self, inurl, chapter):
		url = inurl

		urls = inurl.rsplit('/', 2)
		assert len(urls) == 3
		assert urls[1] == '1'

		url = "/".join((urls[0], str(chapter), urls[2]))

		self.dbFunc.upsert(url, dlstate=0, distance=0, walkLimit=1)

		return url

	def extractSeriesReleases(self, seriesPageUrl):
		soup = self.wg.getSoup(seriesPageUrl)

		titletg  = soup.find("h1", class_='fiction-title')
		authortg = soup.find("span", class_='author')
		ratingtg = soup.find("span", class_='overall')

		assert float(ratingtg['score']) >= MIN_RATING

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
		for text in [para.get_text() for para in paras]:
			if text.lower().startswith('categories:'):
				tagstr = text.split(":", 1)[-1]
				items = tagstr.split(",")
				[tags.append(item.strip()) for item in items if item.strip()]
		extra = {}
		extra['tags']     = tags
		extra['homepage'] = seriesPageUrl

		# print(title, author)
		# print(extra)

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
			vol, chp, frag, post = FeedScrape.FeedDataParser.extractTitle(chp_title)

			raw_item = {}
			raw_item['srcname']   = "RoyalRoadL"
			raw_item['published'] = reldate
			raw_item['linkUrl']   = release.a['href']

			msg = FeedScrape.FeedDataParser.buildReleaseMessage(raw_item, title, vol, chp, frag, author=author, postfix=chp_title, tl_type='oel', extraData=extra)
			retval.append(msg)

		return retval


	def getSeriesPage(self, entry):
		ratingtg = entry.find("span", class_='score')

		if not ratingtg:
			return False

		# Filter poorly rated or unrated series.
		if float(ratingtg['score']) < MIN_RATING:
			return False

		links = entry.find_all("a")
		assert len(links) == 1

		link = links[0]

		assert link.get_text() == "Fiction Page"
		return link['href']

	def parseEntry(self, entry):
		seriesPage = self.getSeriesPage(entry)
		if not seriesPage:
			return []

		releases = self.extractSeriesReleases(seriesPage)
		self.log.info("Found %s releases for series", len(releases))
		return releases

	def loadReleases(self, fromurl):
		soup = self.wg.getSoup(fromurl)

		content = soup.find("ul", id='fiction-list')
		entries = content.find_all("li", class_='fiction mature')

		data = []
		for entry in entries:

			ret = self.parseEntry(entry)
			if ret:
				for item in ret:
					data.append(item)
		self.log.info("Found %s releases from fictionpress", len(data))
		return data



	def getChanges(self):
		for releasePage in self.base:
			releases = self.loadReleases(releasePage)
			self.log.info("Total releases found from RoyalRoadL: %s", len(releases))
			for release in releases:
				# print(release)
				pkt = self.createPacket(release)
				self.amqpint.put_item(pkt)
				# return
				# print(pkt)



	def createPacket(self, data):
		ret = {
			'type' : 'parsed-release',
			'data' : data
		}
		return json.dumps(ret)



class RoyalRoadLTest(RoyalRoadLMonitor):

	tableKey = 'fp'




def test():
	# import logSetup
	# logSetup.initLogging()
	fetch = RoyalRoadLTest()
	fetch.getChanges()
	# fetch.extractSeriesReleases('http://www.royalroadl.com/fiction/1615')


if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()
	test()

