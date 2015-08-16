


import runStatus
runStatus.preloadDicts = False

import WebMirror.OutputFilters.FilterBase


import bs4
import re
import calendar

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




class RRLProcessor(WebMirror.OutputFilters.FilterBase.FilterBase):


	wanted_mimetypes = [

							'text/html',
						]
	want_priority    = 50

	loggerPath = "Main.Filter.RoyalRoad"


	@staticmethod
	def wantsUrl(url):
		if re.search(r"http://www\.royalroadl\.com/fiction/\d+", url):
			print("RRL Wants url: '%s'" % url)
			return True
		return False

	def __init__(self, **kwargs):

		self.kwargs     = kwargs


		self.pageUrl    = kwargs['pageUrl']

		self.content    = kwargs['pgContent']
		self.type       = kwargs['type']

		self.log.info("Processing RSS Item")
		super().__init__()


##################################################################################################################################
##################################################################################################################################
##################################################################################################################################



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


##################################################################################################################################
##################################################################################################################################
##################################################################################################################################



	def extractContent(self):
		print("Call to extract!")


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



	url = 'http://www.royalroadl.com/fiction/3021'

	job = testJobFromUrl(url)
	engine.dispatchRequest(job)




	url = 'http://www.w3schools.com/xml/note.xml'
	job = testJobFromUrl(url)
	engine.dispatchRequest(job)


if __name__ == "__main__":
	test()

