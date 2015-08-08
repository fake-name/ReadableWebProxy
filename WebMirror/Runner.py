
if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()

from concurrent.futures import ProcessPoolExecutor
import WebMirror.rules
import WebMirror.util.urlFuncs as urlFuncs
import time
import multiprocessing
import signal
import logging
import traceback
import WebMirror.Engine

# Global run control value. Only used to stop running processes.
run_state = multiprocessing.Value('i', 1)

def halt_exc(x, y):
	if run_state.value == 0:
		print("Raising Keyboard Interrupt")
		raise KeyboardInterrupt

class RunInstance(object):
	def __init__(self, num, rules):
		signal.signal(signal.SIGINT, signal.SIG_IGN)
		self.num = num
		self.log = logging.getLogger("Main.Text.Web-%s" % num)

		self.archiver = WebMirror.Engine.SiteArchiver()


	def do_task(self):
		self.log.info("Running task!")
		self.archiver.taskProcess()

	def go(self):
		self.log.info("RunInstance starting!")
		while 1:

			if run_state.value:
				self.do_task()
				time.sleep(1)
			else:
				self.log.info("Thread %s exiting.", self.num)
				break


	@classmethod
	def run(cls, num, rules):
		try:
			run = cls(num, rules)
			run.go()
		except Exception:
			print()
			print("Exception in sub-process!")
			traceback.print_exc()

def initializeStartUrls(rules):
	print("Initializing all start URLs in the database")
	import WebMirror.database as db
	print(db)
	print(db.session)

	for ruleset in [rset for rset in rules if rset['starturls']]:
		for starturl in ruleset['starturls']:
			have = db.session.query(db.WebPages)     \
				.filter(db.WebPages.url == starturl) \
				.count()
			if not have:
				netloc = urlFuncs.getNetLoc(starturl)
				new = db.WebPages(
						url      = starturl,
						starturl = starturl,
						netloc   = netloc,
						type     = ruleset['type'],
						priority = db.DB_MED_PRIORITY,
						distance = db.DB_DEFAULT_DIST,
					)
				print("Missing start-url for address: '{}'".format(starturl))
				db.session.add(new)
	db.session.commit()

class Crawler(object):
	def __init__(self):
		self.log = logging.getLogger("Main.Text.Manager")
		self.rules = WebMirror.rules.load_rules()




	def run(self):

		PROCESSES = 20

		executor = ProcessPoolExecutor(max_workers=PROCESSES)

		[executor.submit(RunInstance.run, x, self.rules) for x in range(PROCESSES)]
		try:
			while run_state.value:
				time.sleep(1)
		except KeyboardInterrupt:
			pass

		self.log.info("Crawler allowing ctrl+c to propagate.")
		time.sleep(1)

		run_state.value = 0

		self.log.info("Crawler waiting on executor to complete.")
		try:
			executor.shutdown()
		except KeyboardInterrupt:
			self.log.info("Hard-stopping threads.")
			executor.shutdown(wait=False)

		self.log.info("Executor has shut down.")



if __name__ == "__main__":
	runner = Crawler()
	runner.run()
	print(runner)

