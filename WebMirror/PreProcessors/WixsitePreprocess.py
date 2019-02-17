



import WebMirror.PreProcessors.PreProcessorBase
import urllib.parse
import bs4
import WebRequest



class JsRendererPreprocessor(WebMirror.PreProcessors.PreProcessorBase.ContentPreprocessor):

	loggerPath = "Main.Preprocessor.JsRenderer"

	def clean_content(self, contentstr):

		soup = WebRequest.as_soup(contentstr)

		for bogus in soup.find_all("video"):
			bogus.decompose()
		for bogus in soup.find_all("div", class_="siteBackground"):
			bogus.decompose()


		for div in soup.find_all("main"):
			if 'style' in div.attrs:
				del div.attrs['style']
		for div in soup.find_all("header"):
			if 'style' in div.attrs:
				del div.attrs['style']
		for div in soup.find_all("div"):
			if 'style' in div.attrs:
				del div.attrs['style']

		return soup.prettify()

	def preprocessContent(self, url, mimetype, contentstr):
		soup = WebRequest.as_soup(contentstr)
		text = soup.body.get_text(strip=True).strip()

		if len(text) < 100 or True:
			self.log.info("Page has little or no body. Trying to refetch and render using chromium.")
			contentstr, dummy_fileN, dummy_mType = self.wg_proxy().chromiumGetRenderedItem(url)
		else:
			self.log.info("Page has %s char body, no re-fetch & render needed.", len(text))


		return self.clean_content(contentstr)

	@staticmethod
	def wantsUrl(url):
		netloc = urllib.parse.urlsplit(url).netloc
		if netloc.lower().endswith("wixsite.com"):
			print("JsRendererPreprocessor wants URL: %s", url)
			return True
		if netloc.lower().endswith("catatopatch.com"):
			print("JsRendererPreprocessor wants URL: %s", url)
			return True

		return False
