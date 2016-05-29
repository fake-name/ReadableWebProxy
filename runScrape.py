#!flask/bin/python


if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()

# This HAS to be included before the app, to prevent circular dependencies.
# import WebMirror.runtime_engines

from settings import MAX_DB_SESSIONS
from WebMirror.Runner import NO_PROCESSES
import WebMirror.Runner
import WebMirror.rules
import WebMirror.SpecialCase

def go():

	largv = [tmp.lower() for tmp in sys.argv]

	if not "noreset" in largv:
		print("Resetting any in-progress downloads.")
		WebMirror.Runner.resetInProgress()
	else:
		print("Not resetting in-progress downloads.")

	rules = WebMirror.rules.load_rules()
	WebMirror.Runner.initializeStartUrls(rules)

	global NO_PROCESSES
	global MAX_DB_SESSIONS
	MAX_DB_SESSIONS = NO_PROCESSES + 5

	processes = 50
	NO_PROCESSES = processes
	MAX_DB_SESSIONS = NO_PROCESSES + 5
	if "medianprocesses" in largv:
		processes = 24
		NO_PROCESSES = processes
		MAX_DB_SESSIONS = NO_PROCESSES + 5
	elif "fewprocesses" in largv:
		processes = 6
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

	WebMirror.SpecialCase.startAmqpFetcher()
	runner = WebMirror.Runner.Crawler(thread_count=NO_PROCESSES)
	runner.run()
	WebMirror.SpecialCase.stopAmqpFetcher()

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
