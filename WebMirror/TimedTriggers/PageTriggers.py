

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

		sess = self.db.get_db_session()

		for x in range(len(self.pages)):
			while 1:
				url = self.pages[x]
				if x % 50 == 0:
					self.log.info("Retriggering step %s", x)
				try:
					have = sess.query(self.db.WebPages) \
						.filter(self.db.WebPages.url == url)  \
						.scalar()
					if have and have.state != "new":
						have.state    = "new"
						have.distance = 0
						have.priority = self.db.DB_HIGH_PRIORITY
						have.ignoreuntiltime = datetime.datetime.now() - datetime.timedelta(days=1)
						sess.commit()
						break
					elif have:
						have.ignoreuntiltime = datetime.datetime.now() - datetime.timedelta(days=1)
						have.priority = self.db.DB_HIGH_PRIORITY
						have.distance = 0
						sess.commit()
						# if len(have.versions):
						# 	for item in have.versions[1::]:
						# 		sess.delete(item)
						break
					else:
						new = self.db.WebPages(
								url      = url,
								starturl = url,
								netloc   = urllib.parse.urlsplit(url).netloc,
								priority = self.db.DB_HIGH_PRIORITY,
								distance = 0,
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

		self.log.info("Pages retrigger complete.")

	def go(self):
		self.log.info("Retriggering %s pages.", len(self.pages))
		self.retriggerPages()


class HourlyPageTrigger(PageTriggerBase):
	pages = [
		# RoyalRoadL
		#'http://royalroadl.com/fictions/newest',
		#'http://royalroadl.com/fictions/popular-this-week',
		#'http://royalroadl.com/fictions/best-rated',
		#'http://royalroadl.com/fictions/latest-updates',
		#'http://royalroadl.com/fictions/active-only',
		'http://royalroadl.com/fictions/latest-updates/',
		'http://royalroadl.com/fictions/active-top-50/',
		'http://royalroadl.com/fictions/weekly-views-top-50/',

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
	run = EveryOtherDayPageTrigger()
	run._go()

