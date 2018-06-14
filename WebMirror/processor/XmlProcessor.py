


from . import ProcessorBase

import bs4


class XmlProcessor(ProcessorBase.PageProcessor):


	wanted_mimetypes = ['text/xml', 'application/xml']
	want_priority    = 40

	loggerPath = "Main.Text.XmlProcessor"

	# def __init__(self, pageUrl, loggerPath, content, pbLut, **kwargs):

	def __init__(self, baseUrls, pageUrl, pgContent, loggerPath, relinkable, **kwargs):

		'''
		I'm assuming that pastebin content doesn't have any links, because lazy, mostly.
		'''
		self.loggerPath = (loggerPath+".XmlProcessor")  if not self.loggerPath.endswith(".XmlProcessor") else self.loggerPath
		self.pageUrl    = pageUrl

		self.content    = pgContent
		self.urlLut     = {}


	# Methods to allow the child-class to modify the content at various points.
	def extractTitle(self, content, url):
		return "XML Blob"


	# Process a Google-Doc resource page.
	# This call does a set of operations to permute and clean a google doc page.
	def extractContent(self):

		title = self.extractTitle(self.content, self.pageUrl)

		procContent = bs4.BeautifulSoup(self.content, "xml")
		procContent =  "<pre>" + procContent.prettify() + "</pre>"

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



if __name__ == "__main__":
	test()

