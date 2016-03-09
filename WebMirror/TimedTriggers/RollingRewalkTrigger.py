

import WebMirror.rules
import WebMirror.TimedTriggers.TriggerBase
import config
import datetime
import time
import zlib
import settings
import sqlalchemy.exc

import WebMirror.database as dbm


class RollingRewalkTriggerBase(WebMirror.TimedTriggers.TriggerBase.TriggerBaseClass):


	pluginName = "RollingRewalk Trigger"

	loggerPath = 'RollingRewalk'


	def go(self):
		rules = WebMirror.rules.load_rules()
		self.log.info("Rolling re-trigger of starting URLs.")


		starturls = []
		[starturls.extend(ruleset['starturls']) for ruleset in rules if ruleset and ruleset['starturls']]

		bins = {}

		for url in starturls:
			hval = zlib.crc32(url.encode("utf-8"))
			day = hval % settings.REWALK_INTERVAL_DAYS
			if not day in bins:
				bins[day] = []
			bins[day].append(url)

		today = int(time.time() / (60*60*24)) % settings.REWALK_INTERVAL_DAYS


		if not today in bins:
			return


		threshold_time = datetime.datetime.now() - datetime.timedelta(days=3)

		for url in bins[today]:

			while 1:
				try:
					item = self.db.get_session().query(self.db.WebPages)             \
						.filter(self.db.WebPages.fetchtime < threshold_time)  \
						.filter(self.db.WebPages.state   != "new")            \
						.filter(self.db.WebPages.url == url)             \
						.scalar()
					if not item:
						break
					print(item, item.fetchtime)
					item.state    = "new"
					item.distance = 0
					item.priority = dbm.DB_IDLE_PRIORITY
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

		self.log.info("Old files retrigger complete.")


if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()
	run = RollingRewalkTriggerBase()
	run._go()

