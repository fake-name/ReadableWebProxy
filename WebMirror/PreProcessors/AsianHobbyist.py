



import urllib.parse
import bs4
import WebRequest
import WebMirror.PreProcessors.PreProcessorBase


class AsianHobbyistPreprocessor(WebMirror.PreProcessors.PreProcessorBase.ContentPreprocessor):

	loggerPath = "Main.Preprocessor.AsianHobbyist"


	def preprocessContent(self, url, mimetype, contentstr):
		if mimetype != 'text/html':
			return contentstr

		if isinstance(contentstr, bytes):
			contentstr = bs4.UnicodeDammit(contentstr).unicode_markup

		soup = WebRequest.as_soup(contentstr)

		for bogus in soup.find_all("a", href='https://www.asianhobbyist.com/android-mobile-app-live/'):
			bogus.decompose()

		# There should be some content. If the page is completely empty of text, it was probably an error.
		assert len(soup.get_text(strip=True)) > 50

		return soup.prettify()


	@staticmethod
	def wantsUrl(url):
		return False
		netloc = urllib.parse.urlsplit(url).netloc
		return netloc.lower().endswith("asianhobbyist.com")
