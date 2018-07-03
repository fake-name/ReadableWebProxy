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
import RawArchiver.RawUrlUpserter
import common.stuck
import Misc.ls_open_file_handles

from settings import NO_PROCESSES
from settings import RAW_NO_PROCESSES
from settings import MAX_DB_SESSIONS


def go():

	# fm = Misc.ls_open_file_handles.FileMonitor()
	# fm.patch()

	largv = [tmp.lower() for tmp in sys.argv]


	rules = WebMirror.rules.load_rules()

	runner = common.RunManager.Crawler(main_thread_count=NO_PROCESSES, raw_thread_count=RAW_NO_PROCESSES)

	if "raw" in largv:
		print("RAW Scrape!")
		RawArchiver.RawUrlUpserter.check_init_func()

		if not "noreset" in largv:
			print("Resetting any in-progress downloads.")
			RawArchiver.RawUrlUpserter.resetRawInProgress()
		else:
			print("Not resetting in-progress downloads.")

		RawArchiver.RawUrlUpserter.initializeRawStartUrls()
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
