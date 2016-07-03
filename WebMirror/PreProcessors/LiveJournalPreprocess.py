


import runStatus
runStatus.preloadDicts = False

import WebMirror.PreProcessors.PreProcessorBase
import urllib.parse
import bs4




class LJPreprocessor(WebMirror.PreProcessors.PreProcessorBase.ContentPreprocessor):

	loggerPath = "Main.Preprocessor.Livejournal"

	def acceptAdult(self, content, url):
		soup = bs4.BeautifulSoup(content, "lxml")
		formdiv = soup.find('div', class_='b-msgsystem-warningbox-confirm')

		target = formdiv.form['action']
		bounce = formdiv.input
		button = formdiv.button

		form_args = {
			button['name'] : button['value'],
			bounce['name'] : bounce['value'],
		}

		new = self.wg.getpage(target, postData=form_args)
		assert '<form method="POST" action="http://www.livejournal.com/misc/adult_explicit.bml">' not in new
		return new


	def preprocessContent(self, url, mimetype, contentstr):
		if not isinstance(contentstr, str):
			return contentstr
		self.log.info("Preprocessing content from URL: '%s'", url)
		if '<form method="POST" action="http://www.livejournal.com/misc/adult_explicit.bml">' in contentstr:
			self.log.info("Adult clickwrap page. Stepping through")
			contentstr = self.acceptAdult(contentstr, url)
			self.log.info("Retreived clickwrapped content successfully")
		return contentstr

	@staticmethod
	def wantsUrl(url):
		netloc = urllib.parse.urlsplit(url).netloc
		return netloc.lower().endswith("livejournal.com")
