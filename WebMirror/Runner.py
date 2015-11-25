
if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()

import WebMirror.rules
import WebMirror.util.urlFuncs as urlFuncs
import time
import multiprocessing
import signal
import logging
import traceback
import WebMirror.Engine
import runStatus
import queue
import sqlalchemy.exc
import WebMirror.database as db

import WebMirror.OutputFilters.AmqpInterface
import config
import os.path


from sqlalchemy.sql import text
from sqlalchemy.sql import func
import WebMirror.database as db

# PROCESSES = 24
PROCESSES = 16
# PROCESSES = 4
# PROCESSES = 2
# PROCESSES = 1

# For synchronizing saving cookies to disk
cookie_lock = multiprocessing.Lock()
job_get_lock = multiprocessing.Lock()

def halt_exc(x, y):
	if runStatus.run_state.value == 0:
		print("Raising Keyboard Interrupt")
		raise KeyboardInterrupt

class RunInstance(object):
	def __init__(self, num, rules, response_queue, nosig=True):
		print("RunInstance %s init!" % num)
		if nosig:
			signal.signal(signal.SIGINT, signal.SIG_IGN)
		self.num = num
		self.log = logging.getLogger("Main.Text.Web")

		self.archiver = WebMirror.Engine.SiteArchiver(cookie_lock, job_get_lock=job_get_lock, response_queue=response_queue)
		print("RunInstance %s MOAR init!" % num)


	def do_task(self):
		self.archiver.taskProcess()

	def go(self):
		self.log.info("RunInstance starting!")
		loop = 0
		while 1:
			if runStatus.run_state.value == 1:
				self.do_task()
			else:
				self.log.info("Thread %s exiting.", self.num)
				break
			loop += 1

			if loop == 15:
				loop = 0
				self.log.info("Thread %s awake. Runstate: %s", self.num, runStatus.run_state.value)





	@classmethod
	def run(cls, num, rules, response_queue, nosig=True):
		print("Running!")
		try:
			run = cls(num, rules, response_queue, nosig)
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
			have = db.get_session().query(db.WebPages) \
				.filter(db.WebPages.url == starturl)   \
				.count()
			if not have:
				netloc = urlFuncs.getNetLoc(starturl)
				new = db.WebPages(
						url               = starturl,
						starturl          = starturl,
						netloc            = netloc,
						type              = ruleset['type'],
						priority          = db.DB_IDLE_PRIORITY,
						distance          = db.DB_DEFAULT_DIST,
						normal_fetch_mode = ruleset['normal_fetch_mode'],
					)
				print("Missing start-url for address: '{}'".format(starturl))
				db.get_session().add(new)
		db.get_session().commit()


def resetInProgress():
	print("Resetting any stalled downloads from the previous session.")

	# db.get_session().begin()
	db.get_session().query(db.WebPages) \
		.filter((db.WebPages.state == "fetching") | (db.WebPages.state == "processing"))   \
		.update({db.WebPages.state : "new"})
	db.get_session().commit()


class UpdateAggregator(object):
	def __init__(self, msg_queue):
		self.queue = msg_queue
		self.log = logging.getLogger("Main.Agg.Manager")

		amqp_settings = {
			"RABBIT_LOGIN" : config.C_RABBIT_LOGIN,
			"RABBIT_PASWD" : config.C_RABBIT_PASWD,
			"RABBIT_SRVER" : config.C_RABBIT_SRVER,
			"RABBIT_VHOST" : config.C_RABBIT_VHOST,
		}

		if config.C_DO_RABBIT:
			self._amqpint = WebMirror.OutputFilters.AmqpInterface.RabbitQueueHandler(amqp_settings)

		self.seen = {}

		self.links = 0
		self.amqpUpdateCount = 0
		self.deathCounter = 0

		self.batched_links = []

	def do_amqp(self, pkt):
		self.amqpUpdateCount += 1

		if self.amqpUpdateCount % 50 == 0:
			self.log.info("Transmitted AMQP messages: %s", self.amqpUpdateCount)
		self._amqpint.put_item(pkt)




	def do_link_batch_update(self):
		if not self.batched_links:
			return

		self.log.info("Inserting %s items into DB in batch.", len(self.batched_links))
		while 1:
			try:

				cmd = text("""
						INSERT INTO
							web_pages
							(url, starturl, netloc, distance, is_text, priority, type, fetchtime, state)
						VALUES
							(:url, :starturl, :netloc, :distance, :is_text, :priority, :type, :fetchtime, :state)
						ON CONFLICT DO NOTHING
						""")
				for paramset in self.batched_links:
					db.get_session().execute(cmd, params=paramset)
				db.get_session().commit()
				self.batched_links = []
				break
			except KeyboardInterrupt:
				self.log.info("Keyboard Interrupt?")
				db.get_session().rollback()
			except sqlalchemy.exc.InternalError:
				self.log.info("Transaction error. Retrying.")
				traceback.print_exc()
				db.get_session().rollback()
			except sqlalchemy.exc.OperationalError:
				self.log.info("Transaction error. Retrying.")
				traceback.print_exc()
				db.get_session().rollback()


	def do_link(self, linkdict):
		# print("Link upsert!")
		# Linkdict structure
		# new = {
		# 	'url'       : link,
		# 	'starturl'  : job.starturl,
		# 	'netloc'    : start,
		# 	'distance'  : job.distance+1,
		# 	'is_text'   : istext,
		# 	'priority'  : job.priority,
		# 	'type'      : job.type,
		# 	'state'     : "new",
		# 	'fetchtime' : datetime.datetime.now(),
		# }

		assert 'url'       in linkdict
		assert 'starturl'  in linkdict
		assert 'netloc'    in linkdict
		assert 'distance'  in linkdict
		assert 'is_text'   in linkdict
		assert 'priority'  in linkdict
		assert 'type'      in linkdict
		assert 'state'     in linkdict
		assert 'fetchtime' in linkdict

		url = linkdict['url']

		if not url in self.seen:
			# Fucking huzzah for ON CONFLICT!
			self.batched_links.append(linkdict)
			self.seen[url] = True

			if len(self.batched_links) > 100:
				self.do_link_batch_update()

		# else:
		# 	print("Old item: %s", linkdict)

	def do_task(self):

		target, value = self.queue.get_nowait()

		if (self.links % 50) == 0:
			self.log.info("Aggregator active. Total cached URLs: %s, Items in processing queue: %s, transmitted release messages: %s.", len(self.seen), self.queue.qsize(), self.amqpUpdateCount)

		self.links += 1

		if target == "amqp_msg":
			if config.C_DO_RABBIT:
				self.do_amqp(value)
		elif target == "new_link":
			self.do_link(value)
		else:
			print("Todo", target, value)

	def run(self):

		while 1:
			try:
				self.do_task()
				self.deathCounter = 0
			except queue.Empty:
				if runStatus.agg_run_state.value == 1:
					# Fffffuuuuu time.sleep barfs on KeyboardInterrupt
					try:
						time.sleep(1)
						self.do_link_batch_update()
					except KeyboardInterrupt:
						pass
				else:
					self.do_link_batch_update()
					self.deathCounter += 1
					time.sleep(0.1)
					if self.deathCounter > 5:
						self.log.info("Aggregator thread exiting.")
						break
			except Exception:
				self.log.error("Exception in aggregator!")
				for line in traceback.format_exc():
					self.log.error(line.rstrip())

class Crawler(object):
	def __init__(self):
		self.log = logging.getLogger("Main.Text.Manager")
		self.rules = WebMirror.rules.load_rules()
		self.agg_queue = multiprocessing.Queue()

	def start_aggregator(self):

		agg = UpdateAggregator(self.agg_queue)
		self.agg_proc = multiprocessing.Process(target=agg.run)
		self.agg_proc.start()

	def join_aggregator(self):

		self.log.info("Asking Aggregator process to stop.")
		runStatus.agg_run_state.value = 0
		self.agg_proc.join(0)
		self.log.info("Aggregator joined.")

	def run(self):

		tasks =[]
		cnt = 0
		procno = 0

		self.start_aggregator()

		if PROCESSES == 1:
			self.log.info("Running in single process mode!")
			try:
				RunInstance.run(procno, self.rules, self.agg_queue, nosig=False)
			except KeyboardInterrupt:
				runStatus.run_state.value = 0


		elif PROCESSES < 1:
			self.log.error("Wat?")
		elif PROCESSES > 1:
			try:
				while runStatus.run_state.value:
					time.sleep(1)
					cnt += 1
					if cnt == 10:
						cnt = 0
						living = sum([task.is_alive() for task in tasks])
						for dummy_x in range(PROCESSES - living):
							self.log.warning("Insufficent living child threads! Creating another thread with number %s", procno)
							proc = multiprocessing.Process(target=RunInstance.run, args=(procno, self.rules, self.agg_queue))
							tasks.append(proc)
							proc.start()
							procno += 1
						self.log.info("Living processes: %s", living)

			except KeyboardInterrupt:
				runStatus.run_state.value = 0

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
		self.join_aggregator()


if __name__ == "__main__":
	runner = Crawler()
	runner.run()
	print(runner)

