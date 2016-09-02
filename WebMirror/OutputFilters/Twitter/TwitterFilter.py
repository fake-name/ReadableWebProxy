


import runStatus
runStatus.preloadDicts = False

import WebMirror.OutputFilters.FilterBase

import WebMirror.OutputFilters.util.MessageConstructors  as msgpackers
from WebMirror.OutputFilters.util.TitleParsers import extractTitle

import bs4
import re
import calendar
import unshortenit
import common.util.webFunctions
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

# Because fuck having a proper RSS feed and shit.
NANO_DESU_MAP = {
	'aldnoahextrathetranslation.wordpress.com'      : 'Aldnoah.Zero Extra',
	'www.aldnoahextrathetranslation.wordpress.com'  : 'Aldnoah.Zero Extra',
	'amaburithetranslation.wordpress.com'           : 'Amagi Brilliant Park',
	'www.amaburithetranslation.wordpress.com'       : 'Amagi Brilliant Park',
	'bibliathetranslation.wordpress.com'            : 'Biblia Koshodou no Jiken (Antiquarian Bookshop Biblia’s Case Files)',
	'www.bibliathetranslation.wordpress.com'        : 'Biblia Koshodou no Jiken (Antiquarian Bookshop Biblia’s Case Files)',
	'majonakathetranslation.wordpress.com'          : 'Bokura wa Mahou Shoujo no Naka',
	'www.majonakathetranslation.wordpress.com'      : 'Bokura wa Mahou Shoujo no Naka',
	'fateapocryphathetranslation.wordpress.com'     : 'Fate/Apocrypha',
	'www.fateapocryphathetranslation.wordpress.com' : 'Fate/Apocrypha',
	'firegirlthetranslation.wordpress.com'          : 'Fire Girl',
	'www.firegirlthetranslation.wordpress.com'      : 'Fire Girl',
	'fuyuugakuenthetranslation.wordpress.com'       : 'Fuyuu Gakuen no Alice and Shirley',
	'www.fuyuugakuenthetranslation.wordpress.com'   : 'Fuyuu Gakuen no Alice and Shirley',
	'gekkahimethetranslation.wordpress.com'         : 'Gekka no Utahime to Magi no Ou',
	'www.gekkahimethetranslation.wordpress.com'     : 'Gekka no Utahime to Magi no Ou',
	'gjbuthetranslation.wordpress.com'              : 'GJ-Bu',
	'www.gjbuthetranslation.wordpress.com'          : 'GJ-Bu',
	'www.yamanekothetranslation.wordpress.com'      : 'Goshujin-sama wa Yamaneko-Hime',
	'yamanekothetranslation.wordpress.com'          : 'Goshujin-sama wa Yamaneko-Hime',
	'grimgarthetranslation.wordpress.com'           : 'Hai to Gensou no Grimgar',
	'www.grimgarthetranslation.wordpress.com'       : 'Hai to Gensou no Grimgar',
	'hennekothetranslation.wordpress.com'           : 'Hentai Ouji to Warawanai Neko',
	'www.hennekothetranslation.wordpress.com'       : 'Hentai Ouji to Warawanai Neko',
	'chaikathetranslation.wordpress.com'            : 'Hitsugi no Chaika',
	'www.chaikathetranslation.wordpress.com'        : 'Hitsugi no Chaika',
	'irisorathetranslation.wordpress.com'           : 'Iriya no Sora, UFO no Natsu',
	'www.irisorathetranslation.wordpress.com'       : 'Iriya no Sora, UFO no Natsu',
	'kikoushoujothetranslation.wordpress.com'       : 'Kikou Shoujo wa Kizutsukanai',
	'www.kikoushoujothetranslation.wordpress.com'   : 'Kikou Shoujo wa Kizutsukanai',
	'sekaigamethetranslation.wordpress.com'         : 'Kono Sekai ga Game da to, Ore dake ga Shitteiru',
	'www.sekaigamethetranslation.wordpress.com'     : 'Kono Sekai ga Game da to, Ore dake ga Shitteiru',
	'korezombiethetranslation.wordpress.com'        : 'Kore wa Zombie Desu ka?',
	'www.korezombiethetranslation.wordpress.com'    : 'Kore wa Zombie Desu ka?',
	'kurenaithetranslation.wordpress.com'           : 'Kure-nai',
	'www.kurenaithetranslation.wordpress.com'       : 'Kure-nai',
	'kyousenthetranslation.wordpress.com'           : 'Kyoukai Senjou no Horizon',
	'www.kyousenthetranslation.wordpress.com'       : 'Kyoukai Senjou no Horizon',
	'loveyouthetranslation.wordpress.com'           : 'Love☆You',
	'www.loveyouthetranslation.wordpress.com'       : 'Love☆You',
	'maoyuuthetranslation.wordpress.com'            : 'Maoyuu Maou Yuusha',
	'www.maoyuuthetranslation.wordpress.com'        : 'Maoyuu Maou Yuusha',
	'mayochikithetranslation.wordpress.com'         : 'Mayo Chiki!',
	'www.mayochikithetranslation.wordpress.com'     : 'Mayo Chiki!',
	'magicalgfthetranslation.wordpress.com'         : 'My Girlfriend is a Mahou Shoujo (CN WN)',
	'www.magicalgfthetranslation.wordpress.com'     : 'My Girlfriend is a Mahou Shoujo (CN WN)',
	'ngnlthetranslation.wordpress.com'              : 'No Game, No Life',
	'www.ngnlthetranslation.wordpress.com'          : 'No Game, No Life',
	'ojamajothetranslation.wordpress.com'           : 'Ojamajo Doremi 16',
	'www.ojamajothetranslation.wordpress.com'       : 'Ojamajo Doremi 16',
	'oreimothetranslation.wordpress.com'            : 'Ore no Imouto ga Konna ni Kawaii wake ga Nai',
	'www.oreimothetranslation.wordpress.com'        : 'Ore no Imouto ga Konna ni Kawaii wake ga Nai',
	'qualideascumthetranslation.wordpress.com'      : 'Qualidea of Scum and a Gold Coin',
	'www.qualideascumthetranslation.wordpress.com'  : 'Qualidea of Scum and a Gold Coin',
	'rezerothetranslation.wordpress.com'            : 'Re:Zero Kara Hajimeru Isekai Seikatsu',
	'www.rezerothetranslation.wordpress.com'        : 'Re:Zero Kara Hajimeru Isekai Seikatsu',
	'rokkathetranslation.wordpress.com'             : 'Rokka no Yuusha',
	'www.rokkathetranslation.wordpress.com'         : 'Rokka no Yuusha',
	'saekanothetranslation.wordpress.com'           : 'Saenai Kanojo no Sodatekata',
	'www.saekanothetranslation.wordpress.com'       : 'Saenai Kanojo no Sodatekata',
	'sakurasouthetranslation.wordpress.com'         : 'Sakurasou no Pet na Kanojo',
	'www.sakurasouthetranslation.wordpress.com'     : 'Sakurasou no Pet na Kanojo',
	'sasamisanthetranslation.wordpress.com'         : 'Sasami-san@Ganbaranai',
	'www.sasamisanthetranslation.wordpress.com'     : 'Sasami-san@Ganbaranai',
	'seizonthetranslation.wordpress.com'            : 'Seitokai no Ichizon',
	'www.seizonthetranslation.wordpress.com'        : 'Seitokai no Ichizon',
	'skyworldthetranslation.wordpress.com'          : 'Sky World',
	'www.skyworldthetranslation.wordpress.com'      : 'Sky World',
	'sugardarkthetranslation.wordpress.com'         : 'Sugar Dark',
	'www.sugardarkthetranslation.wordpress.com'     : 'Sugar Dark',
	'vermillionthetranslation.wordpress.com'        : 'Vermillion',
	'www.vermillionthetranslation.wordpress.com'    : 'Vermillion',
	'oregairuthetranslation.wordpress.com'          : 'Yahari Ore no Seishun Love Come wa Machigatteiru',
	'www.oregairuthetranslation.wordpress.com'      : 'Yahari Ore no Seishun Love Come wa Machigatteiru',
	'www.zeromahouthetranslation.wordpress.com'     : 'Zero Kara Hajimeru Mahou no Sho',
	'zeromahouthetranslation.wordpress.com'         : 'Zero Kara Hajimeru Mahou no Sho',
	'bunimithetranslation.wordpress.com'            : 'Bu ni Mi wo Sasagete Hyaku to Yonen. Elf de Yarinaosu Musha Shugyou',
	'www.bunimithetranslation.wordpress.com'        : 'Bu ni Mi wo Sasagete Hyaku to Yonen. Elf de Yarinaosu Musha Shugyou',
}

class TwitterProcessor(WebMirror.OutputFilters.FilterBase.FilterBase):


	wanted_mimetypes = [

							'text/html',
						]
	want_priority    = 50

	loggerPath = "Main.Filter.Twitter"


	@staticmethod
	def wantsUrl(url):
		if url == "https://twitter.com/Baka_Tsuki":
			print("TwitterProcessor want Baka-Tsuki URL")
			return True
		if url == "https://twitter.com/Nano_Desu_Yo":
			print("TwitterProcessor want NanoDesu URL")
			return True
		return False

	def __init__(self, **kwargs):

		self.kwargs     = kwargs


		self.pageUrl    = kwargs['pageUrl']

		self.content    = kwargs['pgContent']
		self.type       = kwargs['type']

		self.log.info("Processing Japtem Item")

		if "dosuper" in kwargs:
			dosuper = kwargs['dosuper']
		else:
			dosuper = True

		if dosuper:
			super().__init__(**kwargs)


		self.log.info("TwitterFilter interface processing content.")


##################################################################################################################################
##################################################################################################################################
##################################################################################################################################

	def sendReleases(self, releases):
		self.log.info("Total releases found on page: %s", len(releases))
		for pkt in releases:
			self.amqp_put_item(pkt)

	def dispatchBT(self, itemurl, itemtxt):
		titleonly = itemtxt.split("by")[0].split("bY")[0].split("By")[0].split("BY")[0]
		probSeries = titleonly.lower().split("volume")[0].split("chapter")[0].strip()

		vol, chp, frag, post = extractTitle(titleonly)

		raw_item = {}
		raw_item['srcname']   = "Baka-Tsuki"
		raw_item['published'] = time.time()
		raw_item['linkUrl']   = itemurl

		self.put_page_link(itemurl)

		msg = msgpackers.buildReleaseMessage(raw_item, probSeries, vol, chp, frag, postfix=post)
		msg = msgpackers.createReleasePacket(msg)

	def dispatchNanoDesu(self, netloc, itemurl, itemtxt):
		itemtitle = NANO_DESU_MAP[netloc]
		vol, chp, frag, post = extractTitle(itemtxt)
		if not (vol or chp):
			return None

		raw_item = {}
		raw_item['srcname']   = "Nano Desu"
		raw_item['published'] = time.time()
		raw_item['linkUrl']   = itemurl

		self.put_page_link(itemurl)

		msg = msgpackers.buildReleaseMessage(raw_item, itemtitle, vol, chp, frag, postfix=post)
		msg = msgpackers.createReleasePacket(msg)
		return msg

	def processPage(self, content):
		soup = common.util.webFunctions.as_soup(self.content)

		releases = []
		for tweet in soup.find_all('li', attrs={"data-item-type":"tweet"}):
			if "promoted" in str(tweet['class']):
				continue
			content = tweet.find("p", class_='tweet-text')
			if content and content.a:
				itemtxt = content.get_text()

				itemurl = content.a['data-expanded-url']
				itemurl, status = unshortenit.unshorten(itemurl)
				if status != 200:
					continue

				urlnl = urllib.parse.urlsplit(itemurl).netloc.lower()
				if urlnl == 'www.baka-tsuki.org':
					msg = self.dispatchBT(itemurl, itemtxt)
					if msg:
						releases.append(msg)
				if urlnl in NANO_DESU_MAP:
					msg = self.dispatchNanoDesu(urlnl, itemurl, itemtxt)
					if msg:
						releases.append(msg)

		self.log.info("Found %s releases from Twitter Feed", len(releases))
		if releases:
			self.sendReleases(releases)



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
	engine.dispatchRequest(testJobFromUrl('https://twitter.com/Baka_Tsuki'))


	# import common.util.webFunctions as webfunc

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

