

import WebMirror.rules
import abc
import WebMirror.TimedTriggers.TriggerBase

import urllib.parse
import sqlalchemy.exc


class PageTriggerBase(WebMirror.TimedTriggers.TriggerBase.TriggerBaseClass):


	pluginName = "Page Triggers"

	loggerPath = 'PageTriggers'

	@abc.abstractproperty
	def pages(self):
		pass


	def retriggerPages(self):

		for url in self.pages:
			while 1:
				try:
					have = self.db.get_session().query(self.db.WebPages) \
						.filter(self.db.WebPages.url == url)  \
						.scalar()
					if have and have.state != "new":
						have.state    = "new"
						have.distance = self.db.MAX_DISTANCE-3
						have.priority = self.db.DB_HIGH_PRIORITY
						self.db.get_session().commit()
						break
					elif have:
						if have.priority != self.db.DB_HIGH_PRIORITY:
							have.priority = self.db.DB_HIGH_PRIORITY
							self.db.get_session().commit()

						if have.distance != self.db.MAX_DISTANCE-3:
							have.distance = self.db.MAX_DISTANCE-3
							self.db.get_session().commit()
						break
					else:
						new = self.db.WebPages(
								url      = url,
								starturl = url,
								netloc   = urllib.parse.urlsplit(url).netloc,
								priority = self.db.DB_HIGH_PRIORITY,
								distance = self.db.MAX_DISTANCE-3,
							)
						self.db.get_session().add(new)
						self.db.get_session().commit()
						break

				except sqlalchemy.exc.InternalError:
					self.log.info("Transaction error. Retrying.")
					self.db.get_session().rollback()
				except sqlalchemy.exc.OperationalError:
					self.log.info("Transaction error. Retrying.")
					self.db.get_session().rollback()
				except sqlalchemy.exc.IntegrityError:
					self.log.info("Transaction error. Retrying.")
					self.db.get_session().rollback()
				except sqlalchemy.exc.InvalidRequestError:
					self.log.info("Transaction error. Retrying.")
					self.db.get_session().rollback()

		self.log.info("Pages retrigger complete.")



	def go(self):
		self.log.info("Retriggering %s pages.", len(self.pages))
		self.retriggerPages()


class HourlyPageTrigger(PageTriggerBase):
	pages = [
		# RoyalRoadL
		'http://royalroadl.com/fictions/best-rated/',
		'http://royalroadl.com/fictions/latest-updates/',
		'http://royalroadl.com/fictions/active-top-50/',
		'http://royalroadl.com/fictions/weekly-views-top-50/',
		'http://royalroadl.com/fictions/newest/',

		# Japtem bits
		'http://japtem.com/fanfic.php?action=last_updated',
		'http://japtem.com/fanfic.php',
	]

class EveryOtherDayPageTrigger(PageTriggerBase):
	rrl_pages    = ['http://www.royalroadl.com/fiction/%s' % x for x in range(5000)]
	japtem_pages = ['http://japtem.com/fanfic.php?novel=%s' % x for x in range(600)]
	pages = rrl_pages + japtem_pages

if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()
	run = HourlyPageTrigger()
	run._go()
	run = EveryOtherDayPageTrigger()
	run._go()

