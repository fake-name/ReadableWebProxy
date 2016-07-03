


import runStatus
runStatus.preloadDicts = False

import WebMirror.PreProcessors.PreProcessorBase
import urllib.parse
import bs4




class TgStoryTimePreprocessor(WebMirror.PreProcessors.PreProcessorBase.ContentPreprocessor):

	loggerPath = "Main.Preprocessor.TgStoryTime"

	def acceptAdult(self, content, url):

		soup = bs4.BeautifulSoup(content, "lxml")
		newloc = soup.find('div', class_='errormsg')
		if not newloc:
			return content
		newloc = newloc.a['href']
		tgt = urllib.parse.urljoin(url, newloc)
		new = self.wg.getpage(tgt)
		assert 'This story has explicit content.' not in new
		return new


	def preprocessContent(self, url, mimetype, contentstr):
		if not isinstance(contentstr, str):
			return contentstr
		self.log.info("Preprocessing content from URL: '%s'", url)
		if 'This story has explicit content.' in contentstr:
			self.log.info("Adult clickwrap page. Stepping through")
			contentstr = self.acceptAdult(contentstr, url)
			self.log.info("Retreived clickwrapped content successfully")
		return contentstr

	@staticmethod
	def wantsUrl(url):
		netloc = urllib.parse.urlsplit(url).netloc
		return netloc.lower().endswith("tgstorytime.com")
