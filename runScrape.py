#!flask/bin/python

if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()

# This HAS to be included before the app, to prevent circular dependencies.
# import WebMirror.runtime_engines

import common.RunManager
import WebMirror.rules
import WebMirror.Runner
import WebMirror.UrlUpserter
import RawArchiver.RawRunner
import common.stuck

from settings import NO_PROCESSES
from settings import RAW_NO_PROCESSES
from settings import MAX_DB_SESSIONS


def go():

	common.stuck.install_pystuck()

	largv = [tmp.lower() for tmp in sys.argv]


	rules = WebMirror.rules.load_rules()

	runner = common.RunManager.Crawler(main_thread_count=NO_PROCESSES, raw_thread_count=RAW_NO_PROCESSES)

	if "raw" in largv:
		print("RAW Scrape!")
		if not "noreset" in largv:
			print("Resetting any in-progress downloads.")
			RawArchiver.UrlUpserter.resetRawInProgress()
		else:
			print("Not resetting in-progress downloads.")

		RawArchiver.UrlUpserter.initializeRawStartUrls()
		runner.run_raw()
	else:

		if not "noreset" in largv:
			print("Resetting any in-progress downloads.")
			WebMirror.UrlUpserter.resetInProgress()
		else:
			print("Not resetting in-progress downloads.")
		WebMirror.UrlUpserter.initializeStartUrls(rules)
		runner.run()


	# print("Thread halted. App exiting.")

if __name__ == "__main__":
	import sys

	largv = [tmp.lower() for tmp in sys.argv]

	if "scheduler" in sys.argv:
		print("Please use runScheduler.py instead!")
		sys.exit(1)
	else:

		started = False
		if not started:
			started = True
			go()
