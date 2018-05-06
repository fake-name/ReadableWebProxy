


import runStatus
runStatus.preloadDicts = False

import WebMirror.PreProcessors.PreProcessorBase
import urllib.parse
import bs4




class RedditPreprocessor(WebMirror.PreProcessors.PreProcessorBase.ContentPreprocessor):

	loggerPath = "Main.Preprocessor.Reddit"

	def acceptAdult(self, content, url):

		target = "https://www.reddit.com/over18?%s" % urllib.parse.urlencode({"dest" : url})

		form_args = {
			"over18" : "yes",
		}

		new = self.wg_proxy().getpage(target, postData=form_args)
		assert '<title>reddit.com: over 18?</title>' not in new
		return new


	def preprocessContent(self, url, mimetype, contentstr):
		if not isinstance(contentstr, str):
			return contentstr
		self.log.info("Preprocessing content from URL: '%s'", url)
		if '<title>reddit.com: over 18?</title>' in contentstr:
			self.log.info("Adult clickwrap page. Stepping through")
			contentstr = self.acceptAdult(contentstr, url)
			self.log.info("Retreived clickwrapped content successfully")
		return contentstr

	@staticmethod
	def wantsUrl(url):
		netloc = urllib.parse.urlsplit(url).netloc
		return netloc.lower().endswith("reddit.com")
