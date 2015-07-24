
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
import WebMirror.Engine
# import rpc

run_state = multiprocessing.Value('i', 1)

def halt_exc(x, y):
	if run_state.value == 0:
		print("Raising Keyboard Interrupt")
		raise KeyboardInterrupt

class RunInstance(object):
	def __init__(self, num, rules):
		import WebMirror.database as db
		signal.signal(signal.SIGINT, halt_exc)
		self.db = db
		self.num = num
		self.rules = rules
		self.log = logging.getLogger("Main.Text.Web-%s" % num)

	def do_task(self):
		self.log.info("Running task!")

	def go(self):
		print("RunInstance starting!")
		while 1:

			if run_state.value:
				self.do_task()
				time.sleep(1)
			else:
				print("Thread", self.num, "exiting.")
				break


	@classmethod
	def run(cls, num, rules):
		run = cls(num, rules)

		run.go()

def initializeStartUrls(rules):
	import WebMirror.database as db
	print(db)
	print(db.session)

	for ruleset in rules:
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
		initializeStartUrls(self.rules)



	def run(self):

		PROCESSES = 4

		executor = ProcessPoolExecutor(max_workers=PROCESSES)

		# [executor.submit(RunInstance.run, x, self.rules) for x in range(PROCESSES)]
		# try:
		# 	while run_state.value:
		# 		time.sleep(1)
		# except KeyboardInterrupt:
		# 	pass

		# self.log.info("Crawler allowing ctrl+c to propagate.")
		# time.sleep(1)

		# run_state.value = 0

		# self.log.info("Crawler waiting on executor to complete.")
		# try:
		# 	executor.shutdown()
		# except KeyboardInterrupt:
		# 	self.log.info("Hard-stopping threads.")
		# 	executor.shutdown(wait=False)

		# self.log.info("Executor has shut down.")



if __name__ == "__main__":
	runner = Crawler()
	runner.run()
	print(runner)

