
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
import runStatus
import WebMirror.database as db

# For synchronizing saving cookies to disk
cookie_lock = multiprocessing.Lock()

def halt_exc(x, y):
	if runStatus.run_state.value == 0:
		print("Raising Keyboard Interrupt")
		raise KeyboardInterrupt

class RunInstance(object):
	def __init__(self, num, rules, nosig=True):
		print("RunInstance %s init!" % num)
		if nosig:
			signal.signal(signal.SIGINT, signal.SIG_IGN)
		self.num = num
		self.log = logging.getLogger("Main.Text.Web")

		self.archiver = WebMirror.Engine.SiteArchiver(cookie_lock)
		print("RunInstance %s MOAR init!" % num)


	def do_task(self):
		self.archiver.taskProcess()

	def go(self):
		self.log.info("RunInstance starting!")
		loop = 0
		while 1:

			if runStatus.run_state.value == 1:
				self.do_task()
				time.sleep(1)
				print("Looping: Thread %s awake. Runstate: %s (value %s)" % (self.num, runStatus.run_state, runStatus.run_state.value))
				print("")
			else:
				self.log.info("Thread %s exiting.", self.num)
				break
			loop += 1

			if loop == 15:
				loop = 0
				self.log.info("Thread %s awake. Runstate: %s (value %s)", self.num, runStatus.run_state, runStatus.run_state.value)


	@classmethod
	def run(cls, num, rules, nosig=True):
		print("Running!")
		try:
			run = cls(num, rules, nosig)
			print("Class instantiated: ", run)
			run.go()
		except Exception:
			print()
			print("Exception in sub-process!")
			traceback.print_exc()

def initializeStartUrls(rules):
	print("Initializing all start URLs in the database")

	for ruleset in [rset for rset in rules if rset['starturls']]:
		for starturl in ruleset['starturls']:
			have = db.get_session().query(db.WebPages)     \
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
				db.get_session().add(new)
	db.get_session().commit()



class Crawler(object):
	def __init__(self):
		self.log = logging.getLogger("Main.Text.Manager")
		self.rules = WebMirror.rules.load_rules()

	def run(self):

		PROCESSES = 8
		tasks =[]
		# executor = ProcessPoolExecutor(max_workers=PROCESSES)
		# tasks = [multiprocessing.Process(target=RunInstance.run, args=(x, self.rules)) for x in range(PROCESSES)]
		# [task.start() for task in tasks]
		cnt = 0
		procno = 0

		if PROCESSES > 1:
			try:
				while runStatus.run_state.value:
					time.sleep(1)
					cnt += 1
					if cnt == 10:
						cnt = 0
						living = sum([task.is_alive() for task in tasks])
						for x in range(PROCESSES - living):
							proc = multiprocessing.Process(target=RunInstance.run, args=(procno, self.rules))
							tasks.append(proc)
							proc.start()
							procno += 1
						self.log.info("Living processes: %s", living)

			except KeyboardInterrupt:
				runStatus.run_state.value = 0
				pass

			self.log.info("Crawler allowing ctrl+c to propagate.")
			time.sleep(1)
			runStatus.run_state.value = 0


			self.log.info("Crawler waiting on executor to complete: Runstate = %s", runStatus.run_state.value)
			while 1:
				living = sum([task.is_alive() for task in tasks])
				[task.join(3.0/(living+1)) for task in tasks]
				self.log.info("Living processes: '%s'", living)
				if living == 0:
					break

			self.log.info("All processes halted.")
		else:
			self.log.info("Running in single process mode!")
			RunInstance.run(procno, self.rules, nosig=False)



if __name__ == "__main__":
	runner = Crawler()
	runner.run()
	print(runner)

