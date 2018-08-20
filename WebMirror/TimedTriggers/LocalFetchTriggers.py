

import settings

import common.database as db
from WebMirror.Engine import SiteArchiver
import WebMirror.TimedTriggers.TriggerBase


class HourlyLocalFetchTrigger(WebMirror.TimedTriggers.TriggerBase.TriggerBaseClass):


	pluginName = "Hourly Local Fetch Trigger"

	loggerPath = 'HourlyLocalFetchTrigger'


	urls = [
		'https://royalroadl.com/api/fiction/updates?apiKey='     + settings.RRL_API_KEY,
		'https://royalroadl.com/api/fiction/newreleases?apiKey=' + settings.RRL_API_KEY,
	]


	def go(self):
		self.log.info("Fetching URLs via local fetcher!")

		for url in self.urls:
			with db.session_context() as sess:
				archiver = SiteArchiver(None, sess, None)
				archiver.synchronousJobRequest(url, ignore_cache=True, debug=True)




if __name__ == "__main__":
	import logSetup
	logSetup.initLogging(1)
	run1 = HourlyLocalFetchTrigger()
	run1._go()
	# run2 = HourlyPageTrigger()
	# run2._go()
	# run3 = EveryOtherDayPageTrigger()
	# run3._go()

