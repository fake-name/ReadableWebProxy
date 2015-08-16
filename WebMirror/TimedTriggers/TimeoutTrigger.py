

import WebMirror.rules
import WebMirror.TimedTriggers.TriggerBase
import config
import datetime

class TimeoutTriggerBase(WebMirror.TimedTriggers.TriggerBase.TriggerBaseClass):


	pluginName = "Timeout Trigger"

	loggerPath = 'TimeoutTrigger'


	def go(self):

		self.log.info("Re-acquiring old files.")

		threshold_time = datetime.datetime.now()-config.REFETCH_INTERVAL

		self.db.get_session().query(self.db.WebPages)             \
			.filter(self.db.WebPages.fetchtime < threshold_time)  \
			.filter(self.db.WebPages.state != "new")              \
			.update({
					self.db.WebPages.state    : "new",
					self.db.WebPages.priority : self.db.DB_LOW_PRIORITY,
				})

		self.db.get_session().commit()



if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()
	run = TimeoutTriggerBase()
	run._go()

