

import WebMirror.rules
import abc
import WebMirror.TimedTriggers.TriggerBase

import urllib.parse
import datetime
import sqlalchemy.exc


class PageTriggerBase(WebMirror.TimedTriggers.TriggerBase.TriggerBaseClass):


	pluginName = "Page Triggers"

	loggerPath = 'PageTriggers'

	@abc.abstractproperty
	def pages(self):
		pass


	def retriggerPages(self):


		for x in range(len(self.pages)):
			url = self.pages[x]
			if x % 50 == 0:
				self.log.info("Retriggering step %s", x)
			self.retriggerUrl(url)

		self.log.info("Pages retrigger complete.")

	def go(self):
		self.log.info("Retriggering %s pages.", len(self.pages))
		self.retriggerPages()


class HourlyPageTrigger(PageTriggerBase):
	pages = [
		# RoyalRoadL
		'http://royalroadl.com/fictions/newest/',
		'http://royalroadl.com/fictions/weekly-views-top-50/',
		'http://royalroadl.com/fictions/latest-updates/',
		'http://royalroadl.com/fictions/active-top-50/',
		'http://royalroadl.com/fictions/best-rated/',

		# Japtem bits
		'http://japtem.com/fanfic.php?action=last_updated',
		'http://japtem.com/fanfic.php',

		# Twitter feeds for annoying sites without better release mechanisms.
		'https://twitter.com/Baka_Tsuki',
		'https://twitter.com/Nano_Desu_Yo',
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

