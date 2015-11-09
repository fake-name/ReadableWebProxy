


import runStatus
runStatus.preloadDicts = False

import WebMirror.OutputFilters.FilterBase

import WebMirror.OutputFilters.util.MessageConstructors  as msgpackers
from WebMirror.OutputFilters.util.TitleParsers import extractTitle

import bs4
import re
import time

from settings import BOOKSIE_REQUIRED_TAGS
from settings import BOOKSIE_MASKED_TAGS

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


# I've done  a lot of scraping of sites with tagging facilities at this point, and I think
# I can say with some certainly people just don't understand what
# tags are a lot of the time.
# Seriously, do people just write random crap in the tag field?
BAD_TAGS = [
	'story',
	'written',
	'by',
	'2',
	'friends.',

	# Apparently, multi-word tags are beyond booksie.
	'science',
	'fiction',
]


IS_BETA = True


class BooksieSeriesPageProcessor(WebMirror.OutputFilters.FilterBase.FilterBase):


	wanted_mimetypes = [

							'text/html',
						]
	want_priority    = 50

	loggerPath = "Main.Filter.Booksie.Page"


	@staticmethod
	def wantsUrl(url):
		if re.search(r"^http://(?:www\.)?booksie\.com/.*?/novel/.*?/chapter/1$", url):
			print("BooksieSeriesPageProcessor Wants url: '%s'" % url)
			return True

		return False

	def __init__(self, **kwargs):

		self.kwargs     = kwargs

		self.pageUrl    = kwargs['pageUrl']

		self.content    = kwargs['pgContent']
		self.type       = kwargs['type']

		self.log.info("Processing Booksie Item")
		super().__init__(**kwargs)


##################################################################################################################################
##################################################################################################################################
##################################################################################################################################


	def extractSeriesReleases(self, seriesPageUrl, soup):

		# Yeah, the title text is in a div with an id of "titlePic".
		# The actual image is in a div with the /class/ titlePic
		# wat.
		titlecontainer = soup.find("div", id='titlePic')
		if not titlecontainer:
			titlecontainer = soup.find("div", id='title')
		if not titlecontainer:
			raise ValueError("No title at URL: '%s'", seriesPageUrl)

		titletg  = titlecontainer.h1
		typetg, authortg, categorytg = titlecontainer.find_all("a")

		if "novel" not in typetg.get_text().lower():
			return []

		if not titletg:
			return []
		if not authortg:
			return []

		title  = titletg.get_text()
		author = authortg.get_text()
		genre  = categorytg.get_text()

		descDiv = soup.find('p', class_='summary')
		for item in descDiv.find_all("a"):
			item.decompose()
		desc = [item.strip() for item in descDiv.find_all(text=True) if item.strip()]


		tagdiv = soup.find("div", id='cloudMain')

		tags = []
		# Skip if no tags
		if tagdiv:
			tags = [item.get_text().strip().lower() for item in tagdiv.find_all("a")]

		tags.append(genre.lower())
		# Fix a lot of the stupid tag fuckups I've seen.
		# People are stupid.
		if 'science' in tags and 'fiction' in tags:
			tags.append("science-fiction")
		tags = [tag for tag in tags if tag not in BAD_TAGS]
		tags = [tag for tag in tags if len(tag) > 2]
		tags = [tag.replace("  ", " ").replace(" ", "-") for tag in tags]
		tags = list(set(tags))


		if not any([tag in BOOKSIE_REQUIRED_TAGS for tag in tags]):
			self.log.info("Missing required tags!")
			return []
		if any([tag in BOOKSIE_MASKED_TAGS for tag in tags]):
			self.log.info("Masked tag!")
			return []

		# Wrap the paragraphs in p tags.
		desc = ['<p>{text}</p>'.format(text=para) for para in desc]

		seriesmeta = {}
		seriesmeta['title']       = title
		seriesmeta['author']      = author
		seriesmeta['tags']        = tags
		seriesmeta['homepage']    = seriesPageUrl
		seriesmeta['desc']        = "\n\n ".join([str(para) for para in desc])
		seriesmeta['tl_type']     = 'oel'
		seriesmeta['sourcesite']  = 'Booksie'

		pkt = msgpackers.sendSeriesInfoPacket(seriesmeta, beta=IS_BETA)

		extra = {}
		extra['tags']     = tags
		extra['homepage'] = seriesPageUrl
		extra['sourcesite']  = 'Booksie'

		# Decompose the announcement (?) div that's cluttering up the
		# search for the chapterdiv
		badchp = soup.find("div", class_='chapters', id='noticeMessage')
		badchp.decompose()

		chapters = soup.find("div", class_='chapters')
		releases = chapters.find_all('a')


		retval = []
		for release in releases:

			# No post time, unfortunately
			chp = int(release.get_text())
			reldate = time.time()

			# Force releases to the beginning of time untill we catch up.
			reldate = 0

			vol  = None
			frag = None

			raw_item = {}
			raw_item['srcname']   = "Booksie"
			raw_item['published'] = reldate
			raw_item['linkUrl']   = release['href']

			msg = msgpackers.buildReleaseMessage(raw_item, title, vol, chp, frag, author=author, tl_type='oel', extraData=extra, beta=IS_BETA)
			retval.append(msg)




		if not retval:
			print("No releases?")
			return []
		self.amqp_put_item(pkt)
		return retval




	def sendReleases(self, releases):
		self.log.info("Total releases found on page: %s. Emitting messages into AMQP local queue.", len(releases))
		for release in releases:
			pkt = msgpackers.createReleasePacket(release, beta=IS_BETA)
			self.amqp_put_item(pkt)




	def processPage(self, url, content):

		soup = bs4.BeautifulSoup(self.content)
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

