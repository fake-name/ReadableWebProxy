


from . import ProcessorBase


import markdown

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




class MarkdownProcessor(ProcessorBase.PageProcessor):


	wanted_mimetypes = ['text/plain']
	want_priority    = 50

	loggerPath = "Main.Text.MarkdownProcessor"

	# def __init__(self, pageUrl, loggerPath, content, pbLut, **kwargs):

	def __init__(self, baseUrls, pageUrl, pgContent, loggerPath, relinkable, **kwargs):

		'''
		I'm assuming that pastebin content doesn't have any links, because lazy, mostly.
		'''
		self.loggerPath = loggerPath+".MarkdownProcessor"
		self.pageUrl    = pageUrl

		self.content    = pgContent
		assert isinstance(pgContent, str), "Content for url %s is not a string" % pageUrl
		self.urlLut     = {}

		# if isinstance(scannedDomains, (set, list)):
		# 	for url in scannedDomains:
		# 		self.installBaseUrl(url)
		# else:
		# 	self.installBaseUrl(scannedDomains)

		# File mapping LUT
		# self.fMap = {}


	# Methods to allow the child-class to modify the content at various points.
	def extractMarkdownTitle(self, content, url):
		# Take the first non-empty line, and just assume it's the title. It'll be close enough.

		prefix = None
		for urlText, prepend in self.urlLut.items():
			if urlText in url:
				prefix = prepend

		if not content:
			return "{prefix} - No content?".format(prefix=prefix)

		tmp1 = content.strip()
		tmp2 = tmp1.split("\n")
		tmp3 = tmp2[0]
		title = tmp3.strip()

		if prefix:
			title = "{prefix} - {title}".format(prefix=prefix, title=title)

		if len(title) > 200:
			title = title[:200] + " [truncated]"

		return title



	# Process a Google-Doc resource page.
	# This call does a set of operations to permute and clean a google doc page.
	def extractContent(self):

		title = self.extractMarkdownTitle(self.content, self.pageUrl)
		procContent = markdown.markdown(self.content)

		self.log.info("Processed title: '%s'", title)
		ret = {}
		# No links here
		ret['plainLinks'] = []
		ret['rsrcLinks']  = []
		ret['title']      = title
		ret['contents']   = procContent

		return ret


def test():
	print("Test mode!")
	import WebRequest
	import logSetup
	logSetup.initLogging()

	# wg = WebRequest.WebGetRobust()
	# # content = wg.getpage('http://www.arstechnica.com')
	# scraper = GdocPageProcessor('https://docs.google.com/document/d/1atXMtCutHRpcHwSRS5UyMAC58_gQjMPR2dDVn1LCD3E', 'Main.Test', 'testinating')
	# print(scraper)
	# extr, rsc = scraper.extractContent()
	# print('Plain Links:')
	# for link in extr['plainLinks']:
	# 	print(link)
	# print()
	# print()
	# print('Resource files:')
	# # for link in extr['rsrcLinks']:
	# # 	print(link)

	# for fName, mimeType, content, pseudoUrl in rsc:
	# 	print(fName, mimeType, pseudoUrl)
	# # print(extr['contents'])



if __name__ == "__main__":
	test()

