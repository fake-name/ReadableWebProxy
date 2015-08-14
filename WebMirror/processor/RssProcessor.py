


import runStatus
runStatus.preloadDicts = False

from . import ProcessorBase


import feedparser

# import TextScrape.RelinkLookup
# import TextScrape.RELINKABLE as RELINKABLE



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




class RssProcessor(ProcessorBase.PageProcessor):


	wanted_mimetypes = [
							'application/atom+xml',
							'application/rdf+xml',
							'application/rss+xml',
							'application/xml',
							'text/xml',
						]
	want_priority    = 50

	loggerPath = "Main.Text.RssProcessor"


	@staticmethod
	def wantsFromContent(content):
		try:
			# Check if the feed has a version
			feed = feedparser.parse(content)
			return bool(feed['version'])
		except Exception:
			return False

	def __init__(self, pageUrl, loggerPath, pgContent, **kwargs):
		'''
		I'm assuming that pastebin content doesn't have any links, because lazy, mostly.
		'''
		self.loggerPath = loggerPath+".RssProcessor"
		self.pageUrl    = pageUrl

		self.content    = pgContent

		self.log.info("Processing RSS Item")


	# @profile
	def parseFeed(self, rawFeed):
		return feedparser.parse(rawFeed)


	# Methods to allow the child-class to modify the content at various points.
	def extractMarkdownTitle(self, content, url):
		# Take the first non-empty line, and just assume it's the title. It'll be close enough.

		prefix = None
		for urlText, prepend in self.urlLut.items():
			if urlText in url:
				prefix = prepend

		title = content.strip().split("\n")[0].strip()

		if prefix:
			title = "{prefix} - {title}".format(prefix=prefix, title=title)

		return title



	# Process a Google-Doc resource page.
	# This call does a set of operations to permute and clean a google doc page.
	def extractContent(self):




		# title = self.extractMarkdownTitle(self.content, self.pageUrl)
		# procContent = markdown.markdown(self.content)

		# self.log.info("Processed title: '%s'", title)

		ret = {}
		# No links here
		ret['plainLinks'] = []
		ret['rsrcLinks']  = []
		ret['title']      = []
		ret['contents']   = []

		return ret


def test():
	print("Test mode!")
	import logSetup
	import WebMirror.rules
	import WebMirror.Fetch
	logSetup.initLogging()


	url = 'http://taulsn.wordpress.com/feed/'
	fetcher = WebMirror.Fetch.ItemFetcher(WebMirror.rules.load_rules(), url, url)
	response = fetcher.fetch()


	url = 'http://fuzionlife.wordpress.com/feed/'
	fetcher = WebMirror.Fetch.ItemFetcher(WebMirror.rules.load_rules(), url, url)
	response = fetcher.fetch()


	url = 'http://www.w3schools.com/xml/note.xml'
	fetcher = WebMirror.Fetch.ItemFetcher(WebMirror.rules.load_rules(), url, url)
	response = fetcher.fetch()


if __name__ == "__main__":
	test()

