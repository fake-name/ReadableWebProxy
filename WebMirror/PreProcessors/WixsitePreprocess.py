


import runStatus
runStatus.preloadDicts = False

import WebMirror.PreProcessors.PreProcessorBase
import urllib.parse
import bs4




class JsRendererPreprocessor(WebMirror.PreProcessors.PreProcessorBase.ContentPreprocessor):

	loggerPath = "Main.Preprocessor.JsRenderer"

	def preprocessContent(self, url, mimetype, contentstr):
		contentstr, fileN, mType = self.wg.chromiumGetRenderedItem(url)
		return contentstr

	@staticmethod
	def wantsUrl(url):
		print("JsRendererPreprocessor for url: %s", url)
		netloc = urllib.parse.urlsplit(url).netloc
		if netloc.lower().endswith("wixsite.com"):
			print("JsRendererPreprocessor wants URL: %s", url)
			return True
		if netloc.lower().endswith("catatopatch.com"):
			print("JsRendererPreprocessor wants URL: %s", url)
			return True

		return False
