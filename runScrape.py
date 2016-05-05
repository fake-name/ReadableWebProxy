#!flask/bin/python

from WebMirror.Runner import NO_PROCESSES
from settings import MAX_DB_SESSIONS
MAX_DB_SESSIONS = NO_PROCESSES + 5

if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()



# This HAS to be included before the app, to prevent circular dependencies.
# import WebMirror.runtime_engines

import WebMirror.Runner
import WebMirror.rules
import runScheduler


def go_test():
	import WebMirror.Engine

	engine = WebMirror.Engine.SiteArchiver(None)
	print(engine)
	for x in range(100):
		engine.getTask()

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


	runner = WebMirror.Runner.Crawler(thread_count=NO_PROCESSES)
	runner.run()

	# print("Thread halted. App exiting.")

def profile():
	import cProfile
	import pstats
	cProfile.run('go()', "run.stats")
	p = pstats.Stats("run.stats")
	p.sort_stats('tottime')
	p.print_stats(250)


def gprofile():
	import cProfile
	import pstats
	from pycallgraph import PyCallGraph
	from pycallgraph.output import GraphvizOutput
	with PyCallGraph(output=GraphvizOutput()):
		go()

if __name__ == "__main__":
	import sys
	print("Auxilliary modes: 'test', 'scheduler'.")


	largv = [tmp.lower() for tmp in sys.argv]

	if "scheduler" in sys.argv:
		global NO_PROCESSES
		global MAX_DB_SESSIONS
		MAX_DB_SESSIONS = 4
		runScheduler.go_sched()
	if "test" in largv:
		go_test()
	elif "profile" in largv:
		profile()
	elif "graph-profile" in largv:
		gprofile()
	else:

		started = False
		if not started:
			started = True

			go()
