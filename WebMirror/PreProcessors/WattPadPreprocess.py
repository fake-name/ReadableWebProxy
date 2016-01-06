


import runStatus
runStatus.preloadDicts = False

import WebMirror.PreProcessors.PreProcessorBase
import urllib.parse
from settings import WATTPAD_AUTH_CREDS



class WattPadPreprocessor(WebMirror.PreProcessors.PreProcessorBase.ContentPreprocessor):

	loggerPath = "Main.Preprocessor.WattPad"



	def check_logged_in(self):
		soup = self.wg.getSoup("https://www.wattpad.com/home")
		uname = soup.find("span", class_='username')
		if uname and WATTPAD_AUTH_CREDS['username'] in uname.get_text():
			return True
		return False

	def doLogin(self, content, url):
		auth = {
			'username' : WATTPAD_AUTH_CREDS['username'],
			'password' : WATTPAD_AUTH_CREDS['password']
		}

		target = "https://www.wattpad.com/login?%s" % urllib.parse.urlencode({"nextUrl" : url})

		content = self.wg.getpage(target, postData=auth)

		now_logged_in = self.check_logged_in()
		if not now_logged_in:
			logger.error("ERROR! Login failed!")
			raise ValueError
		return content


	def preprocessContent(self, url, mimetype, contentstr):
		if not isinstance(contentstr, str):
			return contentstr
		self.log.info("Preprocessing content from URL: '%s'", url)
		if '<a id="header-item-login" rel="nofollow" href=' in contentstr:
			self.log.info("Not logged into wattpad. Rectifying.")
			contentstr = self.doLogin(contentstr, url)
			self.log.info("Wattpad logged in.")
		return contentstr

	@staticmethod
	def wantsUrl(url):
		netloc = urllib.parse.urlsplit(url).netloc
		return netloc.lower().endswith("wattpad.com")
