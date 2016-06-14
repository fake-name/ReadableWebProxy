

import WebMirror.rules
import WebMirror.TimedTriggers.TriggerBase

import urllib.parse
import datetime
import sqlalchemy.exc

class RssTriggerBase(WebMirror.TimedTriggers.TriggerBase.TriggerBaseClass):


	pluginName = "Rss Trigger"

	loggerPath = 'RssTrigger'


	def retriggerRssFeeds(self, feedurls):
		sess = self.db.get_db_session()
		for url in feedurls:
			# print(url)
			self.retriggerUrl(url)


	def go(self):
		self.rules =  WebMirror.rules.load_rules()
		feeds = []
		for item in self.rules:
			feeds += item['feedurls']

		self.log.info("Found %s feeds in rule files.", len(feeds))
		self.retriggerRssFeeds(feeds)



if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()
	run = RssTriggerBase()
	run._go()

