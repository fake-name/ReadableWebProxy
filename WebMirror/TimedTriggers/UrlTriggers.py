

import WebMirror.rules
import abc
import WebMirror.TimedTriggers.TriggerBase

import urllib.parse
import datetime
import sqlalchemy.exc

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
		sess = self.db.get_db_session()

		self.retriggerUrlList(feedurls)


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

		self.retriggerUrlList(self.pages)

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
		'http://royalroadl.com/fictions/new-releases',
		'http://royalroadl.com/fictions/weekly-popular',
		'http://royalroadl.com/fictions/latest-updates',
		'http://royalroadl.com/fictions/active-popular',
		# 'http://royalroadl.com/fictions/best-rated/',

		# Japtem bits
		'http://japtem.com/fanfic.php?action=last_updated',
		'http://japtem.com/fanfic.php',

		# Twitter feeds for annoying sites without better release mechanisms.
		'https://twitter.com/Baka_Tsuki',
		'https://twitter.com/Nano_Desu_Yo',

		# Fetch the new NovelUpdates stuff.
		'http://www.novelupdates.com/',
	]



class EverySixHoursPageTrigger(PageTriggerBase):
	pages = [
		# NovelUpdates
		# 'http://www.novelupdates.com',

	]

class EveryOtherDayPageTrigger(PageTriggerBase):
	rrl_pages    = ['http://www.royalroadl.com/fiction/%s' % x for x in range(10000)]
	japtem_pages = ['http://japtem.com/fanfic.php?novel=%s' % x for x in range(800)]
	pages = rrl_pages + japtem_pages

if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()
	run = HourlyPageTrigger()
	run._go()
	run2 = EveryOtherDayPageTrigger()
	run2._go()

