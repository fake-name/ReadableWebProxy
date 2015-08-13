
import WebMirror.database as db
import WebMirror.rules
import WebMirror.TimedTriggers.TriggerBase

import urllib.parse
import sqlalchemy.exc

class RssTriggerBase(WebMirror.TimedTriggers.TriggerBase.TriggerBaseClass):


	pluginName = "Rss Trigger"

	loggerPath = 'RssTrigger'


	def retriggerRssFeeds(self, feedurls):
		for url in feedurls:
			while 1:
				try:
					have = db.session.query(db.WebPages) \
						.filter(db.WebPages.url == url)  \
						.scalar()
					if have and have.state != "new":
						have.state = "new"
						db.session.commit()
						break
					elif have:
						break
					else:
						new = db.WebPages(
								url      = url,
								starturl = url,
								netloc   = urllib.parse.urlsplit(url).netloc,
								priority = db.DB_HIGH_PRIORITY,
								distance = db.MAX_DISTANCE-2,
							)
						db.session.add(new)
						db.session.commit()
						break

				except sqlalchemy.exc.InternalError:
					self.log.info("Transaction error. Retrying.")
					self.db.session.rollback()
				except sqlalchemy.exc.OperationalError:
					self.log.info("Transaction error. Retrying.")
					self.db.session.rollback()
				except sqlalchemy.exc.IntegrityError:
					self.log.info("Transaction error. Retrying.")
					self.db.session.rollback()
				except sqlalchemy.exc.InvalidRequestError:
					self.log.info("Transaction error. Retrying.")
					self.db.session.rollback()




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

