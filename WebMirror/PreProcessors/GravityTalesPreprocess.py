


import runStatus
runStatus.preloadDicts = False

import WebMirror.PreProcessors.PreProcessorBase
import urllib.parse
import bs4


class GravityTalesPreprocessor(WebMirror.PreProcessors.PreProcessorBase.ContentPreprocessor):

	loggerPath = "Main.Preprocessor.GravityTales"

	def botGarbage(self, content, url):
		errs = 0
		while '<div id="bot-alert" class="alert alert-info">' in content:


			if errs > 1:
				return content

			self.log.info("Trying phantomjs fetch to circumvent recaptcha")
			self.wg_proxy().resetUa()
			content, dummy_name, dummy_mime = self.wg_proxy().getItemPhantomJS(url)
			errs += 1

		return content

	def preprocessContent(self, url, mimetype, contentstr):
		if not isinstance(contentstr, str):
			return contentstr
		self.log.info("Preprocessing content from URL: '%s'", url)
		if '<div id="bot-alert" class="alert alert-info">' in contentstr:
			self.log.info("Bot bullshit. Stepping through.")
			contentstr = self.botGarbage(contentstr, url)
			self.log.info("Retreived clickwrapped content successfully")
		return contentstr

	@staticmethod
	def wantsUrl(url):
		return False
		netloc = urllib.parse.urlsplit(url).netloc
		return netloc.lower().endswith("gravitytales.com")
