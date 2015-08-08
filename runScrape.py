#!flask/bin/python

if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()


import threading
import time
import traceback

import WebMirror.Runner
import WebMirror.rules
import flags

import sys

def go():
	if "init" in sys.argv:

		rules = WebMirror.rules.load_rules()
		WebMirror.Runner.initializeStartUrls(rules)
	else:
		runner = WebMirror.Runner.Crawler()
		runner.run()

	# print("Thread halted. App exiting.")

if __name__ == "__main__":
	started = False
	if not started:
		started = True
		go()
