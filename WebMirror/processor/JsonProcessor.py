


from . import ProcessorBase

import json2html


class JsonProcessor(ProcessorBase.PageProcessor):


	wanted_mimetypes = ['text/json', 'application/json']
	want_priority    = 50

	loggerPath = "Main.Text.JsonProcessor"

	# def __init__(self, pageUrl, loggerPath, content, pbLut, **kwargs):

	def __init__(self, baseUrls, pageUrl, pgContent, loggerPath, relinkable, **kwargs):

		'''
		I'm assuming that pastebin content doesn't have any links, because lazy, mostly.
		'''
		self.loggerPath = (loggerPath+".JsonProcessor")  if not self.loggerPath.endswith(".JsonProcessor") else self.loggerPath
		self.pageUrl    = pageUrl

		self.content    = pgContent
		self.urlLut     = {}


	# Methods to allow the child-class to modify the content at various points.
	def extractMarkdownTitle(self, content, url):
		return "Json Blob"


	# Process a Google-Doc resource page.
	# This call does a set of operations to permute and clean a google doc page.
	def extractContent(self):

		title = self.extractMarkdownTitle(self.content, self.pageUrl)
		procContent = json2html.json2html.convert(json = self.content, table_attributes='id="info-table" class="table table-bordered table-hover"')

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

