

import logging
import abc
import datetime
import urllib.parse
import sqlalchemy.exc
import common.database as db

class TriggerBaseClass(metaclass=abc.ABCMeta):

	# Abstract class (must be subclassed)
	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def pluginName(self):
		return None

	@abc.abstractmethod
	def loggerPath(self):
		return None


	def __init__(self):

		self.db = db

		self.log = logging.getLogger("Main.Trigger."+self.loggerPath)
		self.log.info("Loading %s Runner", self.pluginName)


	def _go(self):
		self.log.info("Checking %s for updates", self.pluginName)

		self.go()
		self.log.info("Update check for %s finished.", self.pluginName)

	def retriggerUrl(self, url, conditional=None):

		sess = self.db.get_db_session()
		while 1:
			try:
				have = sess.query(self.db.WebPages) \
					.filter(self.db.WebPages.url == url)  \
					.scalar()
				if have and have.state in ['disabled', 'specialty_deferred', 'specialty_ready', 'removed']:
					self.log.warning("Page disabled or being processed by specialty handler: (%s, %s)?", have.url, have.state)
				elif conditional and not conditional(have):
					sess.commit()
				elif (
						have
						and have.state in ['new', 'fetching', 'processing', 'removed']
						and have.priority <= self.db.DB_HIGH_PRIORITY
						and have.distance > 1
						and have.ignoreuntiltime > datetime.datetime.now() - datetime.timedelta(hours=1)
					):
					self.log.info("Skipping: '%s' (%s, %s)", url, have.state, have.priority)
				elif have and have.state not in ['new', 'disabled', 'specialty_deferred', 'specialty_ready']:
					self.log.info("Retriggering feed URL: %s", url)
					have.state    = "new"
					have.priority = self.db.DB_HIGH_PRIORITY
					have.ignoreuntiltime = datetime.datetime.now() - datetime.timedelta(days=1)
					sess.commit()
				elif have:
					self.log.warning("URL already in 'new' state: %s", url)
					have.ignoreuntiltime = datetime.datetime.now() - datetime.timedelta(days=1)
					have.priority = self.db.DB_HIGH_PRIORITY
					have.distance = 0
					sess.commit()
				else:
					self.log.info("New URL: %s", url)
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


if __name__ == "__main__":
	import utilities.testBase as tb

	with tb.testSetup(startObservers=True):

		run = Runner()
		run.go()

