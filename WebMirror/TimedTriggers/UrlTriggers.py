

import abc

import WebMirror.rules
import WebMirror.TimedTriggers.TriggerBase
import WebRequest
import settings

class UrlTrigger(WebMirror.TimedTriggers.TriggerBase.TriggerBaseClass):

	@abc.abstractmethod
	def get_urls(self):
		pass



class RssTriggerBase(UrlTrigger):


	pluginName = "Rss Trigger"

	loggerPath = 'RssTrigger'


	def get_urls(self):
		self.rules =  WebMirror.rules.load_rules()
		feeds = []
		for item in self.rules:
			feeds += item['feedurls']
		return feeds


	def retriggerRssFeeds(self, feedurls):
		self.log.info("Retriggering RSS feed URLs")
		sess = self.db.get_db_session()

		self.retriggerUrlList(feedurls, ignoreignore=True)


	def go(self):
		feeds = self.get_urls()
		self.log.info("Found %s feeds in rule files.", len(feeds))
		self.retriggerRssFeeds(feeds)



class PageTriggerBase(UrlTrigger):


	pluginName = "Page Triggers"

	loggerPath = 'PageTriggers'

	@abc.abstractproperty
	def pages(self):
		pass


	def get_urls(self):
		# (hacky) explicit copy
		return [tmp for tmp in self.pages]

	def retriggerPages(self):

		self.retriggerUrlList(self.pages, ignoreignore=True)

		# for x in range(len(self.pages)):
		# 	url = self.pages[x]
		# 	if x % 50 == 0:
		# 		self.log.info("Retriggering step %s", x)
		# 	self.retriggerUrl(url)

		self.log.info("Pages retrigger complete.")

	def go(self):
		self.log.info("Retriggering %s pages.", len(self.pages))
		self.retriggerPages()


class HourlyPageTrigger(PageTriggerBase):
	pages = [
		# RoyalRoadL


		'https://www.royalroad.com/fictions/new-releases',
		# 'https://www.royalroad.com/fictions/weekly-popular',
		'https://www.royalroad.com/fictions/latest-updates',
		# 'https://www.royalroad.com/fictions/active-popular',
		# 'https://www.royalroad.com/fictions/best-rated/',

		# Japtem bits
		'http://japtem.com/fanfic.php?action=last_updated',
		'http://japtem.com/fanfic.php',

		# Twitter feeds for annoying sites without better release mechanisms.
		'https://twitter.com/Baka_Tsuki',
		'https://twitter.com/Nano_Desu_Yo',

		# Fetch the new NovelUpdates stuff.
		'https://www.novelupdates.com/',
	]



class EverySixHoursPageTrigger(PageTriggerBase):
	pages = [
		# NovelUpdates
		# 'http://www.novelupdates.com',

	]

class EveryOtherDayPageTrigger(PageTriggerBase):

	pages = []

	def _rrlExtractSeriesReleases(self, soup):

		containers = soup.find_all('div', class_='fiction-list-item')
		# print(soup)
		# print("container: ", containers)
		if not containers:
			return []
		urls = []
		for item in containers:
			div = item.find('h2', class_='fiction-title')
			a = div.find("a")
			if a:
				sections = a['href'].split("/")
				try:
					sec_int = int(sections[2])
					urls.append(sec_int)
				except ValueError:
					self.log.error("Section isn't an int: '%s'?", sections)
				except IndexError:
					self.log.error("Series URL doesn't appear to be in the expected format: '%s'?", a['href'])
			else:
				self.log.error("No series in container: %s", item)

		return set(urls)


	def get_pages(self):
		wg = WebRequest.WebGetRobust()
		soup = wg.getSoup('https://www.royalroadl.com/fictions/new-releases')
		rrl_max = self._rrlExtractSeriesReleases(soup)

		rrl_pages    = ['http://www.royalroadl.com/fiction/%s' % x for x in range(max(rrl_max))]
		japtem_pages = ['http://japtem.com/fanfic.php?novel=%s' % x for x in range(800)]
		return rrl_pages + japtem_pages

	def go(self):
		self.pages = self.get_pages()
		self.log.info("Retriggering %s pages.", len(self.pages))
		self.retriggerPages()


if __name__ == "__main__":
	import logSetup
	logSetup.initLogging(1)
	run1 = RssTriggerBase()
	run1._go()
	# run2 = HourlyPageTrigger()
	# run2._go()
	# run3 = EveryOtherDayPageTrigger()
	# run3._go()

