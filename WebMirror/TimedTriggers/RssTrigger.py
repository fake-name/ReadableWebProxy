

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
			while 1:
				try:
					have = sess.query(self.db.WebPages) \
						.filter(self.db.WebPages.url == url)  \
						.scalar()
					if have and have.state in ['fetching', 'processing']:
						self.log.warning("Page being processed (%s, %s)?", have.url, have.state)

					if have and have.state in ['disabled', 'specialty_deferred', 'specialty_ready']:
						self.log.warning("Page disabled or being processed by specialty handler: (%s, %s)?", have.url, have.state)
					elif have and have.state not in ['new', 'disabled', 'specialty_deferred', 'specialty_ready']:
						self.log.info("Retriggering feed URL: %s", url)
						have.state    = "new"
						have.priority = self.db.DB_HIGH_PRIORITY
						have.ignoreuntiltime = datetime.datetime.now() - datetime.timedelta(days=1)
						sess.commit()
						break
					elif have:
						self.log.warning("Feed URL already in 'new' state: %s", url)
						have.ignoreuntiltime = datetime.datetime.now() - datetime.timedelta(days=1)
						have.priority = self.db.DB_HIGH_PRIORITY
						have.distance = 0
						sess.commit()
						break
					else:
						self.log.info("New Feed URL: %s", url)
						new = self.db.WebPages(
								url      = url,
								starturl = url,
								netloc   = urllib.parse.urlsplit(url).netloc,
								priority = self.db.DB_HIGH_PRIORITY,
								distance = 0
							)
						sess.add(new)
						sess.commit()
						break

				except sqlalchemy.exc.InternalError:
					self.log.info("Transaction error. Retrying.")
					sess.rollback()
				except sqlalchemy.exc.OperationalError:
					self.log.info("Transaction error. Retrying.")
					sess.rollback()
				except sqlalchemy.exc.IntegrityError:
					self.log.info("Transaction error. Retrying.")
					sess.rollback()
				except sqlalchemy.exc.InvalidRequestError:
					self.log.info("Transaction error. Retrying.")
					sess.rollback()




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

