

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
		for ruleset in [tmp for tmp in rules if (tmp and tmp['starturls'])]:
			for starturl in ruleset['starturls']:
				if not ruleset['rewalk_interval_days']:
					interval = settings.REWALK_INTERVAL_DAYS
				else:
					interval = ruleset['rewalk_interval_days']
				starturls.append((interval, starturl))



		threshold_time = datetime.datetime.now() - datetime.timedelta(days=3)
		sess = self.db.get_db_session()

		for interval, url in starturls:
			hval = zlib.crc32(url.encode("utf-8"))

			day   = hval % interval
			today = int(time.time() / (60*60*24)) % interval

			if "wattpad.com" in url:
				continue
			if "booksie.com" in url:
				continue
			while 1:
				try:
					item = sess.query(self.db.WebPages)             \
						.filter(self.db.WebPages.fetchtime < threshold_time)  \
						.filter(self.db.WebPages.state   != "new")            \
						.filter(self.db.WebPages.url == url)             \
						.scalar()
					if not item:
						break

					if day == today or item.fetchtime < (datetime.datetime.now() - datetime.timedelta(days=settings.REWALK_INTERVAL_DAYS)):
						print("Retriggering: ", item, item.fetchtime, item.url)
						item.state    = "new"
						item.distance = 0
						item.priority = dbm.DB_IDLE_PRIORITY
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

		self.log.info("Old files retrigger complete.")


if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()
	run = RollingRewalkTriggerBase()
	run._go()

