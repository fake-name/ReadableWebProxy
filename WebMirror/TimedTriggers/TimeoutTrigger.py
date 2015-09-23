

import WebMirror.rules
import WebMirror.TimedTriggers.TriggerBase
import config
import datetime
import sqlalchemy.exc


class TimeoutTriggerBase(WebMirror.TimedTriggers.TriggerBase.TriggerBaseClass):


	pluginName = "Timeout Trigger"

	loggerPath = 'TimeoutTrigger'


	def go(self):

		self.log.info("Re-acquiring old files.")

		threshold_time = datetime.datetime.now()-config.REFETCH_INTERVAL
		while 1:
			try:
				self.db.get_session().query(self.db.WebPages)             \
					.filter(self.db.WebPages.fetchtime < threshold_time)  \
					.filter(self.db.WebPages.state   != "new")            \
					.filter(self.db.WebPages.is_text != True)             \
					.update({
							self.db.WebPages.state    : "new",
							self.db.WebPages.priority : self.db.DB_LOW_PRIORITY,
						})

				self.db.get_session().commit()

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


if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()
	run = TimeoutTriggerBase()
	run._go()

