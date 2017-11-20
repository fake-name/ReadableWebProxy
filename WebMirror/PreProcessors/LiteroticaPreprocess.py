


import runStatus
runStatus.preloadDicts = False

import WebMirror.PreProcessors.PreProcessorBase
import urllib.parse
import bs4




class LiteroticaFavouritePreprocessor(WebMirror.PreProcessors.PreProcessorBase.ContentPreprocessor):

	loggerPath = "Main.Preprocessor.Literotica.FavouritePreprocessor"

	def unwrap_favourites(self, content, url):

		soup = bs4.BeautifulSoup(content, "lxml")
		favp = soup.find('p', class_='b-favorites-users')
		if not favp:
			return content

		if not favp.span:
			return content
		if not favp.span.get('title', None):
			return content

		favurl_fmt = "https://search.literotica.com/search.php?type=member&q={user}"

		unames = favp.span.get('title')
		unamel = unames.split(",")
		unamel = [tmp.strip() for tmp in unamel]

		for uname in unamel:

			linka           = soup.new_tag("a")
			linka['href']   = favurl_fmt.format(user=uname)
			linka.string    = uname

			favp.append(linka)


		return soup.prettify()


	def preprocessContent(self, url, mimetype, contentstr):
		if not isinstance(contentstr, str):
			return contentstr
		self.log.info("Preprocessing content from URL: '%s'", url)
		if 'favorited this story!' in contentstr:
			self.log.info("Flattening favourites!")
			contentstr = self.unwrap_favourites(contentstr, url)
			self.log.info("Converted favourite dialog for series.")
		return contentstr

	@staticmethod
	def wantsUrl(url):
		netloc = urllib.parse.urlsplit(url).netloc
		return netloc.lower().endswith("literotica.com")
