


import runStatus
runStatus.preloadDicts = False

import WebMirror.OutputFilters.FilterBase

import WebMirror.OutputFilters.util.MessageConstructors  as msgpackers
from WebMirror.OutputFilters.util.TitleParsers import extractTitle
# from WebMirror.Engine import SiteArchiver

import bs4
import re
import calendar
import time
from dateutil.parser import parse
import urllib.parse
from WebMirror.util.webFunctions import WebGetRobust

import WebMirror.API
import pprint

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

IS_BETA = False


class LNDBSeriesPageFilter(WebMirror.OutputFilters.FilterBase.FilterBase):


	wanted_mimetypes = [

							'text/html',
						]
	want_priority    = 50

	loggerPath = "Main.Filter.LNDB"


	@staticmethod
	def wantsUrl(url):
		if re.search(r"^http://lndb.info/light_novel/.+$", url):
			if "lndb.info/light_novel/view/" in url:
				return False
			# print("LNDB Processor Wants url: '%s'" % url)
			return True
		return False

	def __init__(self, **kwargs):

		self.kwargs     = kwargs
		self.job        = kwargs['job']

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

		itemsoup = self.getSoupForSeriesItem(seriesPageUrl, soup)
		itemdata = self.extractSeriesInfo(itemsoup)
		# print(itemdata)

		tags = []
		if 'genre' in itemdata and itemdata['genre']:
			tags = list(set([item.lower().strip().replace("  ", " ").replace(" ", "-") for item in itemdata['genre']]))

		seriesmeta = {}


		seriesmeta['title']       = itemdata['title']
		seriesmeta['alt_titles']  = [itemdata['jTitle'], ] + itemdata['alt_names']


		seriesmeta['author']      = itemdata['author']
		seriesmeta['illust']      = itemdata['illust']
		seriesmeta['desc']        = itemdata['description']
		if itemdata['pubdate']:
			seriesmeta['pubdate']     = calendar.timegm(itemdata['pubdate'].timetuple())
		else:
			seriesmeta['pubdate']     = None
		seriesmeta['pubnames']    = itemdata['pubnames']


		seriesmeta['tags']        = tags
		seriesmeta['homepage']    = None

		seriesmeta['tl_type']     = 'translated'
		seriesmeta['sourcesite']  = 'LNDB'


		# pprint.pprint(itemdata)
		# pprint.pprint(seriesmeta)

		# print(seriesmeta)
		pkt = msgpackers.sendSeriesInfoPacket(seriesmeta, beta=IS_BETA)
		self.amqp_put_item(pkt)



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

	def getSoupForSeriesItem(self, baseUrl, baseSoup):
		urlpostfix = baseUrl.replace("http://lndb.info/light_novel/", "")

		# print("urlpostfix:", urlpostfix)

		url      = urllib.parse.urljoin('http://lndb.info/', '/light_novel/view/' + urlpostfix)
		referrer = urllib.parse.urljoin('http://lndb.info/', '/light_novel/' + urlpostfix)

		soup = None
		for x in range(3):
			try:
				# You have to specify the 'X-Requested-With' param, or you'll get a 404
				content = self.wg.getpage(url, addlHeaders={'Referer': referrer, 'X-Requested-With': 'XMLHttpRequest'})
				# print("Wat wat?")
				WebMirror.API.processFetchedContent(url, content, "text/html", self.job)
				soup = bs4.BeautifulSoup(content)
				break
			except urllib.error.URLError:
				time.sleep(4)
				# Randomize the user agent again
				self.wg = webFunctions.WebGetRobust(logPath=self.loggerPath+".Web")
		if not soup:
			raise ValueError("Could not retreive page!")

		return soup

	def getPubDate(self, soup):
		pubdate = None
		pubnames = []

		pubdiv1 = soup.find("div", class_='lightnovellabels')
		pubdiv2 = soup.find("div", class_='lightnovelmagazines')



		for pubdiv in [item for item in [pubdiv1, pubdiv2] if item]:
			for item in pubdiv.find_all("p", class_='paragraph-info'):
				for publink in item.find_all("a"):
					pub = publink.get_text().strip()
					if not pub in pubnames:
						pubnames.append(pub)

				children = list(item.children)
				for x in range(len(children)):

					if children[x]:
						if str(children[x]).startswith("\xa0"):
							dates = str(children[x])
							if "-" in dates:
								dates = dates.split("-")[0].strip()
								ts = parse(dates, fuzzy=True)
								if not pubdate:
									pubdate = ts
								else:
									if ts < pubdate:
										pubdate = ts

		return pubdate, pubnames

	def getAltNames(self, soup):
		pubdiv = soup.find("div", class_='lightnovelassociatedtitles')
		if pubdiv:
			for item in pubdiv.find_all("p", class_='paragraph-info'):
				return [item.strip() for item in item.stripped_strings]
		return None

	def getDescription(self, soup):
		pubdiv = soup.find("div", class_='lightnovelabout')
		if pubdiv:
			return " ".join([str(item) for item in pubdiv.find_all("p", class_='paragraph-info')])
		return None

	def extractSeriesInfo(self, soup):
		content = soup.find('div', class_='lightnovelcontent')

		dataLut = {
			'Japanese Title'        : 'jTitle',
			'Volume Title'          : 'oTitle',
			'Japanese Volume Title' : 'jvTitle',
			'Light Novel'           : 'series',
			'Publisher'             : 'pub',
			'Light Novel Label'     : 'label',
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

		mdataLut = {
			'Author'                : 'author',
			'Illustrator'           : 'illust',
			'Illustrators'          : 'illust',
		}

		assert content != None



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

		for tr in rows:
			tds = tr.find_all('td')
			if len(tds) != 2:
				self.log.error("Row with wrong number of items?")
				continue
			desc, cont = tds
			desc = desc.get_text().strip()
			cont = cont.get_text().strip()

			if desc in mdataLut:
				kwargs[mdataLut[desc]] = [item.strip() for item in cont.split(",")]

		itemTitle = content.find('div', class_='secondarytitle').get_text().strip()
		kwargs['title'] = itemTitle

		if "genre" in kwargs:
			kwargs['genre'] = [item.strip().lower() for item in kwargs['genre'].split(",")]
		else:
			kwargs['genre'] = []

		altn = self.getAltNames(content)
		if altn:
			kwargs['alt_names'] = altn
		else:
			kwargs['alt_names'] = []

		desc = self.getDescription(content)
		if desc:
			kwargs['description'] = desc
		else:
			kwargs['description'] = None

		pubdate, pubnames = self.getPubDate(content)
		if pubdate:
			kwargs['pubdate'] = pubdate
		else:
			kwargs['pubdate'] = None
		if pubnames:
			kwargs['pubnames'] = pubnames
		else:
			kwargs['pubnames'] = None


		return kwargs





	def processPage(self, url, content):

		soup = bs4.BeautifulSoup(self.content)

		self.extractSeries(self.pageUrl, soup)






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
	import WebMirror.Engine
	import multiprocessing
	logSetup.initLogging()

	c_lok = cookie_lock = multiprocessing.Lock()
	engine = WebMirror.Engine.SiteArchiver(cookie_lock=c_lok)



	engine.dispatchRequest(testJobFromUrl('http://lndb.info/light_novel/Gamers!'))
	engine.dispatchRequest(testJobFromUrl('http://lndb.info/light_novel/AntiMagic_Academy_The_35th_Test_Platoon'))
	engine.dispatchRequest(testJobFromUrl('http://lndb.info/light_novel/Madan_no_Ou_to_Vanadis'))
	engine.dispatchRequest(testJobFromUrl('http://lndb.info/light_novel/Aru_Hi,_Bakudan_ga_Ochitekite'))
	# engine.dispatchRequest(testJobFromUrl('http://www.royalroadl.com/fictions/latest-updates'))



if __name__ == "__main__":
	test()

