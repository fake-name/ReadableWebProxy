
#!/usr/bin/python
# from profilehooks import profile

import abc
import feedparser
import FeedScrape.RssMonitorDbBase
import TextScrape.utilities.Proxy
import FeedScrape.FeedDataParser
import calendar
import json
import bs4
import TextScrape.RelinkLookup
import urllib.error
import FeedScrape.AmqpInterface
import readability.readability
# import TextScrape.RELINKABLE as RELINKABLE
import parsedatetime
import datetime
# pylint: disable=W0201
#
import TextScrape.HtmlProcessor
import urllib.parse

class EmptyFeedError(Exception):
	pass

# buildReleaseMessage(raw_item, series, vol, chap=None, frag=None, postfix='')

class FictionPressMonitor(FeedScrape.RssMonitorDbBase.RssDbBase, FeedScrape.FeedDataParser.DataParser):

	tableName = 'western_monitor'

	loggerPath = 'Main.Rss.Fp'

	# Has to be explicitly overridden, or the inheritnace will
	# asplode.
	log = None
	test_override = []
	htmlProcClass = TextScrape.HtmlProcessor.HtmlPageProcessor


	# All english content
	# Can't filter out poetry at this point, unfortunately (arrrgh)
	root = 'https://www.fictionpress.com'
	base = 'https://www.fictionpress.com/j/0/0/1/'

	def __init__(self):
		super().__init__()

		self.dbFunc = TextScrape.utilities.Proxy.EmptyProxy(tableKey='fictionpress', tableName='book_western_items', scanned=[self.root])
		if not hasattr(self, 'wg'):
			import webFunctions
			self.wg = webFunctions.WebGetRobust(logPath='Main.Text.Feed.Web')

	def getTime(self, tups, raw_soup):
		spans = raw_soup.find_all('span')
		for span in spans:
			ts = span.get('data-xutime')
			if ts:
				val = int(ts)
				return float(val)

		pubtm = tups['Published'].strip()
		if len(pubtm) <= 3:
			pubtm += " ago"
		cal = parsedatetime.Calendar()
		ulDate, status = cal.parse(pubtm)
		ulDate = datetime.datetime(*ulDate[:6])

		return calendar.timegm(ulDate.timetuple())


	def patchUrl(self, inurl, chapter):
		url = inurl

		urls = inurl.rsplit('/', 2)
		assert len(urls) == 3
		assert urls[1] == '1'

		url = "/".join((urls[0], str(chapter), urls[2]))

		self.dbFunc.upsert(url, dlstate=0, distance=0, walkLimit=1)

		return url

	def parseEntry(self, entry):

		titletg = entry.find("a", class_='stitle')
		metadiv = entry.find("div", class_='xgray')
		if not titletg:
			return False

		# Don't want to trigger on review items
		if entry.find("a", class_='reviews'):
			return False

		title = titletg.get_text().strip()
		url   = urllib.parse.urljoin(self.base, titletg['href'])

		metatxt = metadiv.get_text()
		meta = [item.strip() for item in metatxt.split("-")]
		tups = dict([item.split(":") for item in meta if ":" in item])

		if not "Fiction" in tups:
			return False
		if not "Chapters" in tups:
			return False
		if not "Published" in tups:
			return False
		if not "Words" in tups:
			return False

		chapters = int(tups['Chapters'])
		wordcount = int(tups['Words'].replace(",", ""))

		if chapters < 3:
			return False

		# Filter some really frivilous fluff bullshit.
		if wordcount < 2500:
			return False

		url = self.patchUrl(url, chapters)
		raw_item = {}
		raw_item['srcname']   = "FictionPress"
		raw_item['published'] = self.getTime(tups, entry)
		raw_item['linkUrl']   = url

		release = FeedScrape.FeedDataParser.buildReleaseMessage(raw_item, title, None, chapters, author=None, tl_type='oel')


		return release

	def loadReleases(self, fromurl):
		soup = self.wg.getSoup(fromurl)

		content = soup.find("div", id='content_wrapper_inner')
		entries = content.find_all("div", class_='zpointer')

		data = []
		for entry in entries:

			ret = self.parseEntry(entry)
			if ret:
				data.append(ret)

		self.log.info("Found %s releases from fictionpress", len(data))
		return data



	def getChanges(self):
		releases = self.loadReleases(self.base)
		for release in releases:
			print(release)
			pkt = self.createPacket(release)
			self.amqpint.put_item(pkt)



	def createPacket(self, data):
		ret = {
			'type' : 'parsed-release',
			'data' : data
		}
		return json.dumps(ret)



class FictionPressTest(FictionPressMonitor):

	tableKey = 'fp'




def test():
	# import logSetup
	# logSetup.initLogging()
	fetch = FictionPressTest()
	fetch.getChanges()


if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()
	test()

