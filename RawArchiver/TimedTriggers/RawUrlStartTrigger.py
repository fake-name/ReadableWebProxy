

import config
import urllib.parse
import datetime
import traceback
import time
# import tqdm
import zlib
import settings
import datetime
import sqlalchemy.exc
from sqlalchemy import or_
from sqlalchemy import and_
from sqlalchemy import func
from sqlalchemy import text
import common.database as dbm

import RawArchiver.RawActiveModules
import RawArchiver.TimedTriggers.TriggerBase
import RawArchiver.misc as raw_misc
import RawArchiver.RawUrlUpserter


class RollingRawUrlStartTrigger(RawArchiver.TimedTriggers.TriggerBase.TriggerBaseClass):


	pluginName = "RollingRewalk Trigger"

	loggerPath = 'Main.RollingRawRewalker'


	def retrigger_urls(self, url_list):
		self.log.info("Retrigging %s urls", len(url_list))


		with self.db.session_context(override_timeout_ms=1000*60*15) as sess:
			for url in url_list:
				epoch = raw_misc.get_epoch_for_url(url)
				nl = urllib.parse.urlsplit(url).netloc

				linksd = [{
					'url'             : url,
					'starturl'        : url,
					'netloc'          : nl,
					'distance'        : dbm.DB_DEFAULT_DIST,
					'priority'        : dbm.DB_MED_PRIORITY,
					'state'           : "new",
					'addtime'         : datetime.datetime.now(),

					# Don't retrigger unless the ignore time has elaped.
					'epoch' : raw_misc.get_epoch_for_url(url, nl),
					}]

				RawArchiver.RawUrlUpserter.do_link_batch_update_sess(self.log, sess, linksd)

				row = sess.query(self.db.RawWebPages)       \
					.filter(self.db.RawWebPages.url == url) \
					.scalar()

				print(row, row.state, row.epoch)


	def go(self):

		print("Startup?")


		self.log.info("Rolling re-trigger of starting URLs.")

		starturls = []
		for module in RawArchiver.RawActiveModules.ACTIVE_MODULES:
			for url in module.get_start_urls():

				nl = urllib.parse.urlsplit(url).netloc
				self.log.info("Interval: %s, netloc: %s", module.rewalk_interval, nl)
				starturls.append(url)


		self.retrigger_urls(starturls)



if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()
	run = RollingRawRewalkTrigger()
	run.go()
	# run._go()

