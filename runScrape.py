#!flask/bin/python

if __name__ == "__main__":
	import logSetup
	import logging
	logSetup.initLogging()
	# logSetup.initLogging(logging.WARNING)

	# Shut up fucking annoying psycopg2 vomit every exec.
	import warnings
	from sqlalchemy import exc as sa_exc
	warnings.filterwarnings("ignore", category=UserWarning, module='psycopg2')
	warnings.simplefilter("ignore", category=sa_exc.SAWarning)


# This HAS to be included before the app, to prevent circular dependencies.
# import WebMirror.runtime_engines


import multiprocessing
import time
import common.RunManager
import WebMirror.rules
import WebMirror.Runner
import WebMirror.UrlUpserter
import RawArchiver.RawRunner
import RawArchiver.RawUrlUpserter
import common.stuck
import common.process
import Misc.ls_open_file_handles

import common.redis
import common.management.WebMirrorManage

from settings import NO_PROCESSES
from settings import RAW_NO_PROCESSES
from settings import MAX_DB_SESSIONS


def go(args):

	largv = [tmp.lower() for tmp in args]


	rules = WebMirror.rules.load_rules()

	runner = common.RunManager.Crawler(main_thread_count=NO_PROCESSES, raw_thread_count=RAW_NO_PROCESSES)

	if "raw" in largv:
		common.process.name_process("raw fetcher management thread")
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

		common.process.name_process("fetcher management thread")
		if not "noreset" in largv:
			print("Resetting any in-progress downloads.")
			WebMirror.UrlUpserter.resetInProgress()
			WebMirror.UrlUpserter.resetRedisQueues()
		else:
			print("Not resetting in-progress downloads.")

		#if not "noreset" in largv:
		#	print("Dropping fetch priority levels.")
		#	common.management.WebMirrorManage.exposed_drop_priorities()

		#else:
		#	print("Not resetting fetch priority levels.")


		WebMirror.UrlUpserter.initializeStartUrls(rules)


		runner.run()
		print("Main runner returned!")


	# print("Thread halted. App exiting.")

def run_in_subprocess():
	pass

	proc = multiprocessing.Process(target=go, args=(sys.argv, ))
	proc.start()
	while proc.is_alive():
		time.sleep(10)
		print("Base Subprocessor Runner")

	print("Main runner has gone away. Committing Suicide")

	# If the subprocess has gone away, die hard.
	import ctypes;ctypes.string_at(1)
	import os;os.kill(0,4)

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
			run_in_subprocess()
