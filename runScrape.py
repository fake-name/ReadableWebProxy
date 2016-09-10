#!flask/bin/python


if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()

# This HAS to be included before the app, to prevent circular dependencies.
# import WebMirror.runtime_engines

from settings import MAX_DB_SESSIONS
import common.RunManager
import WebMirror.rules
import WebMirror.Runner
import RawArchiver.RawRunner



NO_PROCESSES = 24
# NO_PROCESSES = 12
# NO_PROCESSES = 8
# NO_PROCESSES = 4
# NO_PROCESSES = 2
# NO_PROCESSES = 1


RAW_NO_PROCESSES = 5


def go():

	import pystuck; pystuck.run_server()

	largv = [tmp.lower() for tmp in sys.argv]

	if not "noreset" in largv:
		print("Resetting any in-progress downloads.")
		WebMirror.Runner.resetInProgress()
		RawArchiver.RawRunner.resetInProgress()
	else:
		print("Not resetting in-progress downloads.")

	rules = WebMirror.rules.load_rules()
	WebMirror.Runner.initializeStartUrls(rules)
	RawArchiver.RawRunner.initializeRawStartUrls()


	global NO_PROCESSES
	global MAX_DB_SESSIONS
	MAX_DB_SESSIONS = NO_PROCESSES + 5

	processes = 16
	NO_PROCESSES = processes
	MAX_DB_SESSIONS = NO_PROCESSES + 5
	if "maxprocesses" in largv:
		processes = 24
		NO_PROCESSES = processes
		MAX_DB_SESSIONS = NO_PROCESSES + 5
	elif "fewprocesses" in largv:
		processes = 8
		NO_PROCESSES = processes
		MAX_DB_SESSIONS = NO_PROCESSES + 5
	elif "twoprocess" in largv:
		processes = 2
		NO_PROCESSES = processes
		MAX_DB_SESSIONS = NO_PROCESSES + 2
	elif "oneprocess" in largv:
		processes = 1
		NO_PROCESSES = processes
		MAX_DB_SESSIONS = NO_PROCESSES + 2

	runner = common.RunManager.Crawler(main_thread_count=NO_PROCESSES, raw_thread_count=RAW_NO_PROCESSES)
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
