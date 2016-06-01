#!flask/bin/python

import settings
if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()

# This HAS to be included before the app, to prevent circular dependencies.
# import WebMirror.runtime_engines
# WebMirror.runtime_engines.init_engines()

from app import app
import threading
import time
import calendar

# import FeedFeeder.FeedFeeder
import flags




def thread_run():
	interface = None
	while flags.RUNSTATE:
		try:
			if not interface:
				interface = FeedFeeder.FeedFeeder.FeedFeeder()
			interface.process()
		except Exception:
			print("Attempting to reconnect. Please stand by.")
			interface = None
			time.sleep(10)
		time.sleep(1)


def startBackgroundThread():
	print("ThreadStarter")

	bk_thread = threading.Thread(target = thread_run)
	bk_thread.start()
	return bk_thread


def go():
	flags.IS_FLASK = True
	settings.MAX_DB_SESSIONS = 10

	import sys

	if not "debug" in sys.argv:
		print("Starting background thread")
		# bk_thread = startBackgroundThread()

	if "debug" in sys.argv:
		print("Running in debug mode.")
		app.run(host='0.0.0.0', port=5001)
	else:
		print("Running in normal mode.")
		# app.run(host='0.0.0.0', port=5001, processes=10)
		app.run(host='0.0.0.0', port=5001, threaded=True)


	print()
	print("Interrupt!")
	# if not "debug" in sys.argv:
	# 	print("Joining on background thread")
	# 	flags.RUNSTATE = False
	# 	bk_thread.join()

	# print("Thread halted. App exiting.")

if __name__ == "__main__":
	started = False
	if not started:
		started = True
		go()
