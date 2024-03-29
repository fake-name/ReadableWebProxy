

import settings

import common.database as db
from WebMirror.Engine import SiteArchiver
import WebMirror.TimedTriggers.TriggerBase


class RRLLocalFetchTrigger(WebMirror.TimedTriggers.TriggerBase.TriggerBaseClass):


	pluginName = "RRL Local Fetch Trigger"

	loggerPath = 'HourlyLocalFetchTrigger'

	urls = [

		# Todo: move to better fetch infrastructure.
		# 'https://www.novelupdates.com',
		# 'https://www.novelupdates.com/?pg=2',
		# 'https://www.novelupdates.com/?pg=3',
		# 'https://www.novelupdates.com/?pg=4',
		# 'https://www.novelupdates.com/?pg=5',

		'https://www.scribblehub.com/latest-series/',
		'https://www.scribblehub.com/latest-series/?pg=2',
		'https://www.scribblehub.com/latest-series/?pg=3',
		'https://www.scribblehub.com/series-ranking/?sort=3&order=1',

		"https://www.scribblehub.com/rssfeed.php?type=main",

		'https://royalroad.com/api/fiction/updates?apiKey='     + settings.RRL_API_KEY,
		'https://royalroad.com/api/fiction/newreleases?apiKey=' + settings.RRL_API_KEY,
	]


	def go(self):
		self.log.info("Fetching URLs via local fetcher!")

		for url in self.urls:
			with db.session_context() as sess:
				archiver = SiteArchiver(None, sess, None)
				archiver.synchronousJobRequest(url, ignore_cache=True, debug=True)




if __name__ == "__main__":
	import logSetup
	# logSetup.initLogging(1)
	logSetup.initLogging()
	run1 = RRLLocalFetchTrigger()
	run1._go()