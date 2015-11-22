


import runStatus
runStatus.preloadDicts = False

import WebMirror.OutputFilters.FilterBase

import WebMirror.OutputFilters.util.MessageConstructors  as msgpackers
from WebMirror.OutputFilters.util.TitleParsers import extractTitle

import bs4
import re
import markdown
import time
import datetime
import calendar
import urllib.parse
from WebMirror.util.webFunctions import WebGetRobust

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

BLOCK_IDS = {

}



IS_BETA = True


class LNDBSeriesPageFilter(WebMirror.OutputFilters.FilterBase.FilterBase):


	wanted_mimetypes = [

							'text/html',
						]
	want_priority    = 50

	loggerPath = "Main.Filter.LNDB"


	@staticmethod
	def wantsUrl(url):
		if re.search(r"^http://lndb.info/light_novel/.+$", url):
			# print("LNDB Processor Wants url: '%s'" % url)
			return True
		return False

	def __init__(self, **kwargs):

		self.kwargs     = kwargs


		self.pageUrl    = kwargs['pageUrl']

		self.content    = kwargs['pgContent']
		self.type       = kwargs['type']

		self.log.info("Processing RSS Item")
		super().__init__()

		self.wg = WebGetRobust(logPath=self.loggerPath+".Web")


##################################################################################################################################
##################################################################################################################################
##################################################################################################################################


	def extractSeries(self, seriesPageUrl, soup):

		itemsoup = self.getSoupForSeriesItem(seriesPageUrl)
		itemdata = self.extractSeriesInfo(itemsoup)
		print(itemdata)

		# title  = metadata['title']
		# author = metadata['user']['name']
		# desc   = metadata['description']
		# tags   = metadata['tags']

		# # Apparently the description is rendered in a <pre> tag.
		# # Huh?
		# desc = markdown.markdown(desc, extensions=["linkify"])

		# title = title.strip()

		# # Siiiiiigh. Really?
		# title = title.replace("[#wattys2015]", "")
		# title = title.replace("(Wattys2015) ", "")
		# title = title.replace("#Wattys2015", "")
		# title = title.replace("Wattys2015", "")
		# title = title.strip()

		# if metadata['numParts'] < 3:
		# 	return []
		# if metadata['voteCount'] < 100:
		# 	return []

		# # Language ID 1 is english.
		# if metadata['language']['id'] != 1:
		# 	return []

		# # Allow blocking of item by ID
		# if metadata['id'] in BLOCK_IDS:
		# 	return []

		# # for some particularly stupid reasons, the item category tag is
		# # not included in the metadata.
		# # therefore, we parse it out from the page manually.
		# tagdiv = soup.find("div", class_="tags")
		# if tagdiv:
		# 	for tag in tagdiv.find_all("a", class_='tag'):
		# 		tags.append(tag.get_text())


		# tags = list(set([item.lower().strip().replace("  ", " ").replace(" ", "-") for item in tags]))

		# # Mask any content with any of the blocked tags.
		# if any([item in tags for item in LNDB_MASKED_TAGS]):
		# 	self.log.warning("Item has a masked tag. Not emitting any releases.")
		# 	self.log.warning("Tags: '%s'", tags)
		# 	return

		# # And check that at least one of the target tags is present.
		# if not any([item in tags for item in LNDB_REQUIRED_TAGS]):
		# 	self.log.warning("Item missing required tag. Not emitting any releases.")
		# 	self.log.warning("Tags: '%s'", tags)
		# 	return


		# seriesmeta = {}

		# extra = {}
		# extra['tags']        = tags[:]
		# extra['homepage']    = seriesPageUrl
		# extra['sourcesite']  = 'LNDB'



		# retval = []
		# index = 1
		# valid = 1
		# for release in metadata['parts']:
		# 	chp_title = release['title']

		# 	dt = datetime.datetime.strptime(release['modifyDate'], "%Y-%m-%dT%H:%M:%SZ" )
		# 	reldate = calendar.timegm(dt.timetuple())

		# 	raw_item = {}
		# 	raw_item['srcname']   = "LNDB"
		# 	raw_item['published'] = reldate
		# 	raw_item['linkUrl']   = release['url']
		# 	msg = msgpackers.buildReleaseMessage(raw_item, title, None, index, None, author=author, postfix=chp_title, tl_type='oel', extraData=extra, beta=IS_BETA)
		# 	retval.append(msg)

		# 	# Check if there was substantive structure in the chapter
		# 	# name. Used as a crude heuristic for chapter validity.
		# 	# vol, chp, frag, post = extractTitle(chp_title)
		# 	# if any((vol, chp, frag)):
		# 	# 	# print("Valid: ", (vol, chp, frag))
		# 	# 	valid += 1

		# 	index += 1

		# # if valid < (index/2):
		# # 	print("Half the present chapters are have no numeric content?")
		# # 	return []

		# # Don't send the series metadata if we didn't find any chapters.
		# if not retval:
		# 	print("No chapters!")
		# 	return []


		# seriesmeta['title']       = title
		# seriesmeta['author']      = author
		# seriesmeta['tags']        = tags
		# seriesmeta['homepage']    = seriesPageUrl
		# seriesmeta['desc']        = desc
		# seriesmeta['tl_type']     = 'oel'
		# seriesmeta['sourcesite']  = 'LNDB'


		# pkt = msgpackers.sendSeriesInfoPacket(seriesmeta, beta=IS_BETA)
		# self.log.info("LNDB scraper generated %s amqp messages!", len(retval) + 1)
		# self.amqp_put_item(pkt)
		# return retval



	'''
	Source items:
	seriesEntry - Is this the entry for a series, or a individual volume/chapter
	cTitle      - Chapter Title (cleaned for URL use)
	oTitle      - Chapter Title (Raw, can contain non-URL safe chars)
	jTitle      - Title in Japanese
	vTitle      - Volume Title
	jvTitle     - Japanese Volume Title
	series      - Light Novel
	pub	        - Publisher
	label       - Light Novel Label
	volNo       - Volumes
	author      - Author
	illust      - Illustrator
	target      - Target Readership
	relDate     - Release Date
	covers      - Cover Array
	'''

	def getSoupForSeriesItem(self, baseUrl):
		urlpostfix = baseUrl.replace("http://lndb.info/light_novel/", "")

		print("urlpostfix:", urlpostfix)

		url      = urllib.parse.urljoin('http://lndb.info/', '/light_novel/view/' + urlpostfix)
		referrer = urllib.parse.urljoin('http://lndb.info/', '/light_novel/' + urlpostfix)

		soup = None
		for x in range(3):
			try:
				# You have to specify the 'X-Requested-With' param, or you'll get a 404
				soup = self.wg.getSoup(url, addlHeaders={'Referer': referrer, 'X-Requested-With': 'XMLHttpRequest'})
				break
			except urllib.error.URLError:
				time.sleep(4)
				# Randomize the user agent again
				self.wg = webFunctions.WebGetRobust(logPath=self.loggerPath+".Web")
		if not soup:
			raise ValueError("Could not retreive page!")
		return soup

	def extractSeriesInfo(self, soup):
		content = soup.find('div', class_='lightnovelcontent')

		dataLut = {
			'Japanese Title'        : 'jTitle',
			'Volume Title'          : 'oTitle',
			'Japanese Volume Title' : 'jvTitle',
			'Light Novel'           : 'series',
			'Publisher'             : 'pub',
			'Light Novel Label'     : 'label',
			'Author'                : 'author',
			'Illustrator'           : 'illust',
			'Target Readership'     : 'target',
			'Volumes'               : 'volNo',
			'Release Date'          : 'relDate',
			'Genre'                 : 'genre',
			'Pages'                 : None,
			'ISBN-10'               : None,
			'ISBN-13'               : None,
			'Height (cm)'           : None,
			'Width (cm)'            : None,
			'Thickness (cm)'        : None,
			'Online Shops'          : None,
		}

		assert content != None
		itemTitle = content.find('div', class_='secondarytitle').get_text().strip()

		infoDiv = content.find('div', class_="secondary-info")

		rows = infoDiv.find_all('tr')

		self.log.info("Found %s data rows for item!", len(rows))

		kwargs = {}

		for tr in rows:
			tds = tr.find_all('td')
			if len(tds) != 2:
				self.log.error("Row with wrong number of items?")
				continue
			desc, cont = tds
			desc = desc.get_text().strip()
			cont = cont.get_text().strip()

			if desc in dataLut:
				kwargs[dataLut[desc]] = cont

		return kwargs





	def processPage(self, url, content):

		soup = bs4.BeautifulSoup(self.content)

		releases = self.extractSeries(self.pageUrl, soup)


		if releases:
			self.sendReleases(releases)



	def sendReleases(self, releases):
		self.log.info("Total releases found on page: %s", len(releases))
		for release in releases:
			pkt = msgpackers.createReleasePacket(release, beta=IS_BETA)
			self.amqp_put_item(pkt)



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
	import multiprocessing
	logSetup.initLogging()

	c_lok = cookie_lock = multiprocessing.Lock()
	engine = WebMirror.Engine.SiteArchiver(cookie_lock=c_lok)



	engine.dispatchRequest(testJobFromUrl('http://www.royalroadl.com/fiction/3021'))
	# engine.dispatchRequest(testJobFromUrl('http://www.royalroadl.com/fictions/latest-updates'))



if __name__ == "__main__":
	test()

