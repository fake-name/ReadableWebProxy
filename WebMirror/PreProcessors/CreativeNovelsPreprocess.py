


import runStatus
runStatus.preloadDicts = False

import WebMirror.PreProcessors.PreProcessorBase
import urllib.parse
import bs4
import WebRequest



class CreativeNovelsPreprocessor(WebMirror.PreProcessors.PreProcessorBase.ContentPreprocessor):

	loggerPath = "Main.Preprocessor.JsRenderer"

	def preprocessContent(self, url, mimetype, contentstr):
		if mimetype != 'text/html':
			return contentstr

		if isinstance(contentstr, bytes):
			contentstr = bs4.UnicodeDammit(contentstr).unicode_markup

		soup = WebRequest.as_soup(contentstr)
		next_chp_links = soup.find_all("a", class_='nextkey')
		prev_chp_links = soup.find_all("a", class_='prevkey')

		for tag in next_chp_links:
			tag.string = "Next chapter"
		for tag in prev_chp_links:
			tag.string = "Previous chapter"

		for bogus in soup.find_all("div", class_='x-modal-content'):
			bogus.decompose()
		for bogus in soup.find_all("div", class_='wpdiscuz_unauth'):
			bogus.decompose()
		for bogus in soup.find_all("div", class_='wpd-default'):
			bogus.decompose()
		for bogus in soup.find_all("div", class_='imagepost'):
			bogus.decompose()
		for bogus in soup.find_all("div", class_='donation'):
			bogus.decompose()
		for bogus in soup.find_all("form", class_='x-search'):
			bogus.decompose()
		for bogus in soup.find_all("ul", class_='x-menu'):
			bogus.decompose()
		for bogus in soup.find_all("div", class_='comments-area'):
			bogus.decompose()
		for bogus in soup.find_all("div", class_='respond'):
			bogus.decompose()
		for bogus in soup.find_all("div", class_='x-bar-space-v'):
			bogus.decompose()
		for bogus in soup.find_all("div", class_='e23-20'):
			bogus.decompose()
		for bogus in soup.find_all("button"):
			bogus.decompose()

		appends = []
		for item in soup.find_all('div', class_='togglepost'):
			# print("found append")
			appends.append(item.extract())

		tgtdiv = soup.find("article", class_='post')

		if tgtdiv:
			tgtdiv = tgtdiv.parent.parent
			tgtdiv.append(soup.new_tag('hr'))
			for append in appends:
				# print("Appending:", append)
				tgtdiv.append(append)

		return soup.prettify()

	@staticmethod
	def wantsUrl(url):
		netloc = urllib.parse.urlsplit(url).netloc
		if netloc.lower().endswith("creativenovels.com"):
			print("CreativeNovelsPreprocessor wants URL: %s" % url)
			return True

		return False
