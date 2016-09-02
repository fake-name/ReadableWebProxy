

import WebMirror.rules
import WebMirror.TimedTriggers.TriggerBase
import config
import datetime
import time
import zlib
import settings
import datetime
import sqlalchemy.exc

import common.database as dbm



class RollingRewalkTriggerBase(WebMirror.TimedTriggers.TriggerBase.TriggerBaseClass):


	pluginName = "RollingRewalk Trigger"

	loggerPath = 'RollingRewalk'


	def go(self):
		print()
		print()
		print("FIX ME")
		print()
		print()
		print()
		return

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

			def conditional_check(row):
				if day == today or row.fetchtime < (datetime.datetime.now() - datetime.timedelta(days=settings.REWALK_INTERVAL_DAYS)):
					print("Retriggering: ", row, row.fetchtime, row.url)
					row.state    = "new"
					row.distance = 0
					row.priority = dbm.DB_IDLE_PRIORITY
					row.ignoreuntiltime = datetime.datetime.now() - datetime.timedelta(days=1)

			self.retriggerUrl(url, conditional=conditional_check)


		self.log.info("Old files retrigger complete.")


if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()
	run = RollingRewalkTriggerBase()
	run._go()

