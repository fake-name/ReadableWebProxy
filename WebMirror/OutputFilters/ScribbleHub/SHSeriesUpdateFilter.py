


import re
import WebRequest
import common.util.urlFuncs
import WebMirror.OutputFilters.FilterBase


class SHSeriesUpdateFilter(WebMirror.OutputFilters.FilterBase.FilterBase):


	wanted_mimetypes = [

							'text/html',
						]
	want_priority    = 50

	loggerPath = "Main.Filter.ScribbleHub.Series"


	match_re = re.compile(r"^^https://www\.scribblehub\.com/(?:series-ranking|latest-series)/.*$", flags=re.IGNORECASE)

	@classmethod
	def wantsUrl(cls, url):
		if cls.match_re.search(url):
			print("SHSeriesUpdateFilter Wants url: '%s'" % url)
			return True
		# else:
			print("SHSeriesUpdateFilter doesn't want url: '%s'" % url)

		return False



	def __init__(self, **kwargs):

		self.kwargs     = kwargs


		self.pageUrl    = kwargs['pageUrl']

		self.content    = kwargs['pgContent']
		self.type       = kwargs['type']
		self.db_sess    = kwargs['db_sess']

		self.log.info("Processing ScribbleHub SeriesUpdate Item")
		super().__init__(**kwargs)


##################################################################################################################################
##################################################################################################################################
##################################################################################################################################


	def extractSeriesReleases(self, seriesPageUrl, soup):

		containers = soup.find_all('div', class_='search_main_box')
		# print(soup)
		# print("container: ", containers)
		if not containers:
			return []
		urls = []
		for item in containers:
			div = item.find('div', class_='search_title')
			a = div.find("a")
			if a:
				url = common.util.urlFuncs.rebaseUrl(url=a['href'], base=seriesPageUrl)
				urls.append(url)
			else:
				self.log.error("No series in container: %s", item)

		return set(urls)


	def retrigger_pages(self, releases):
		self.log.info("Total releases found on page: %s. Forcing retrigger of item pages.", len(releases))

		for release_url in releases:
			self.retrigger_page(release_url)





	def processPage(self, url, content):
		print("processPage() call")
		soup = WebRequest.as_soup(self.content)
		releases = self.extractSeriesReleases(self.pageUrl, soup)
		if releases:
			self.retrigger_pages(releases)




##################################################################################################################################
##################################################################################################################################
##################################################################################################################################



	def extractContent(self):
		# print("Call to extract!")
		# print(self.amqpint)

		self.processPage(self.pageUrl, self.content)



def test():
	print("Test mode!")
	import logSetup
	from WebMirror.Engine import SiteArchiver
	import common.database as db

	logSetup.initLogging()

	def fetch(url):
		with db.session_context() as sess:
			archiver = SiteArchiver(
					cookie_lock   = None,
					db_interface  = sess,
					new_job_queue = None
				)
			archiver.synchronousJobRequest(url, ignore_cache=True, debug=True)





	# engine.dispatchRequest(testJobFromUrl('http://www.ScribbleHub.com/fiction/3021'))
	# engine.dispatchRequest(testJobFromUrl('http://www.ScribbleHub.com/fictions/latest-updates/'))

	# engine.dispatchRequest(testJobFromUrl('http://www.ScribbleHub.com/fictions/best-rated/'))
	# fetch('https://www.scribblehub.com/series-ranking/')
	fetch('https://www.scribblehub.com/series-ranking/?sort=3&order=1')
	# fetch('https://www.scribblehub.com/latest-series/')



if __name__ == "__main__":
	test()

