


import runStatus
runStatus.preloadDicts = False

from . import ProcessorBase


import feedparser
import bs4
import json
import calendar
import WebRequest
import WebMirror.OutputFilters.rss.FeedDataParser

# import TextScrape.RelinkLookup
# import TextScrape.RELINKABLE as RELINKABLE


import WebMirror.processor.HtmlProcessor


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




class WattPadJsonProcessor(ProcessorBase.PageProcessor):


	wanted_mimetypes = [
							'text/json',
							'application/json',

							# Sometimes, the content-type is broken somehow. Not sure why
							'text/plain',
						]

	# Priority is higher because we want text/plain items
	# before the markdown processor can get them.
	want_priority    = 60

	loggerPath = "Main.Text.WattPadJsonProcessor"



	def __init__(self, **kwargs):

		self.kwargs     = kwargs

		self.loggerPath = kwargs['loggerPath']+".WattPadJsonProcessor"
		self.pageUrl    = kwargs['pageUrl']

		self.content    = kwargs['pgContent']
		self.type       = kwargs['type']

		self.log.info("Processing WattPad JSON Item")
		super().__init__()

	@staticmethod
	def wantsUrl(url):
		if "www.wattpad.com/api/v3/" in url:
			return True
		return False


	def buildPage(self, data):
		'''
		Build up a simple disambiguation page for the links.
		'''

		if data:
			title = "WattPad Stories Container"
		else:
			return "(empty) WattPad Stories Container", '~~Nothing here~~', []

		soup = WebRequest.as_soup()
		container = soup.new_tag("div")
		soup.append(container)

		links = []

		for item in data:
			links.append(item['url'])

			tmp = soup.new_tag("div")
			h3 = soup.new_tag("h3")
			link = soup.new_tag("a", href=item['url'])
			link.string = item['title']
			h3.append(link)
			tmp.append(h3)

			if 'description' in item and item['description']:
				p = soup.new_tag('p')
				p.string = item['description']
				tmp.append(p)
			container.append(tmp)



		content = soup.prettify()

		return title, content, links


	def extractContent(self):
		ret = {}

		ret['plainLinks'] = []
		ret['rsrcLinks']  = []
		ret['title']      = ""
		ret['contents']   = ""

		try:
			unpacked = json.loads(self.content)
		except Exception:
			self.log.error("Failure to decode content!")
			self.log.error("Page content:")
			self.log.error("'%s'", self.content)
			raise

		if "nextUrl" in unpacked:
			# print("nextUrl:", unpacked['nextUrl'])
			ret['plainLinks'].append(unpacked['nextUrl'])

		if "stories" in unpacked:
			ret['title'], ret['contents'], newLinks = self.buildPage(unpacked['stories'])
			ret['plainLinks'] += newLinks

		# print("Link #", len(ret['plainLinks']))
		return ret




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



	job = testJobFromUrl(r'https://www.wattpad.com/api/v3/stories?fields%3Dstories%28id%2Ctitle%2Curl%2Cdescription%29%2Ctotal%2CnextUrl&limit=50&offset=0')
	engine.dispatchRequest(job)

	job = testJobFromUrl(r'https://www.wattpad.com/api/v3/stories?fields%3Dstories%28id%2Ctitle%2Curl%2Cdescription%29%2Ctotal%2CnextUrl&limit=50&offset=1490')
	engine.dispatchRequest(job)

	job = testJobFromUrl(r'https://www.wattpad.com/api/v3/stories?fields%3Dstories%28id%2Ctitle%2Curl%2Cdescription%29%2Ctotal%2CnextUrl&limit=50&offset=1500')
	engine.dispatchRequest(job)

	job = testJobFromUrl(r'https://www.wattpad.com/api/v3/stories?fields%3Dstories%28id%2Ctitle%2Curl%2Cdescription%29%2Ctotal%2CnextUrl&limit=50&offset=1550')
	engine.dispatchRequest(job)


if __name__ == "__main__":
	test()

