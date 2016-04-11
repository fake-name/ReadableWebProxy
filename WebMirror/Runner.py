
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

NO_PROCESSES = 24
# NO_PROCESSES = 16
# NO_PROCESSES = 4
# NO_PROCESSES = 2
# NO_PROCESSES = 1

# For synchronizing saving cookies to disk
COOKIE_LOCK  = multiprocessing.Lock()
JOB_GET_LOCK = multiprocessing.Lock()

from pympler.tracker import SummaryTracker, summary, muppy
import tracemalloc
import objgraph
import random
import gc

def halt_exc(x, y):
	if runStatus.run_state.value == 0:
		print("Raising Keyboard Interrupt")
		raise KeyboardInterrupt

class RunInstance(object):
	def __init__(self, num, response_queue, cookie_lock, job_get_lock, nosig=True):
		print("RunInstance %s init!" % num)
		if nosig:
			signal.signal(signal.SIGINT, signal.SIG_IGN)
		self.num = num
		self.log = logging.getLogger("Main.Text.Web")
		self.resp_queue = response_queue
		self.cookie_lock = cookie_lock
		self.job_get_lock = job_get_lock

		print("RunInstance %s MOAR init!" % num)

	def __del__(self):
		db.delete_db_session()

	def do_task(self):

		self.db_handle = db.get_db_session()

		self.archiver = WebMirror.Engine.SiteArchiver(self.cookie_lock, job_get_lock=self.job_get_lock, response_queue=self.resp_queue, db_interface=self.db_handle)
		self.archiver.taskProcess()
		# Clear out the sqlalchemy state
		self.db_handle.expunge_all()
		db.delete_db_session()

	def go(self):

		tracemalloc.start()
		self.log.info("RunInstance starting!")
		loop = 0

		# We have to only let the child threads run for a period of time, or something
		# somewhere in sqlalchemy appears to be leaking memory.
		for dummy_x in range(500):
			if runStatus.run_state.value == 1:
				# objgraph.show_growth(limit=3)
				self.do_task()
			else:
				self.log.info("Thread %s exiting.", self.num)
				break
			loop += 1

			if loop == 15:
				loop = 0
				self.log.info("Thread %s awake. Runstate: %s", self.num, runStatus.run_state.value)





	@classmethod
	def run(cls, num, response_queue, cookie_lock, job_get_lock, nosig=True):
		print("Running!")
		try:
			run = cls(num, response_queue, cookie_lock, job_get_lock, nosig)
			print("Class instantiated: ", run)
			run.go()
		except Exception:
			print()
			print("Exception in sub-process!")
			traceback.print_exc()

def initializeStartUrls(rules):
	print("Initializing all start URLs in the database")
	sess = db.get_db_session()
	for ruleset in [rset for rset in rules if rset['starturls']]:
		for starturl in ruleset['starturls']:
			have = sess.query(db.WebPages) \
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
				sess.add(new)
		sess.commit()
	sess.close()
	db.delete_db_session()
def resetInProgress():
	print("Resetting any stalled downloads from the previous session.")

	sess = db.get_db_session()
	sess.query(db.WebPages) \
		.filter((db.WebPages.state == "fetching") | (db.WebPages.state == "processing"))   \
		.update({db.WebPages.state : "new"})
	sess.commit()
	sess.close()
	db.delete_db_session()

class UpdateAggregator(object):
	def __init__(self, msg_queue, db_interface):
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

		self.db_int = db_interface

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
					self.db_int.execute(cmd, params=paramset)
				self.db_int.commit()
				self.batched_links = []
				break
			except KeyboardInterrupt:
				self.log.info("Keyboard Interrupt?")
				self.db_int.rollback()
			except sqlalchemy.exc.InternalError:
				self.log.info("Transaction error. Retrying.")
				traceback.print_exc()
				self.db_int.rollback()
			except sqlalchemy.exc.OperationalError:
				self.log.info("Transaction error. Retrying.")
				traceback.print_exc()
				self.db_int.rollback()
		self.db_int.close()


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


		# The seen dict was eating all my free memory (I think).
		if len(self.seen) > 1000000:
			self.seen = {}

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
	@classmethod
	def launch_agg(cls, agg_queue):
		agg_db = db.get_db_session()
		instance = cls(agg_queue, agg_db)
		instance.run()

class Crawler(object):
	def __init__(self, thread_count=NO_PROCESSES):
		self.log = logging.getLogger("Main.Text.Manager")
		WebMirror.rules.load_rules()
		self.agg_queue = multiprocessing.Queue()

		self.log.info("Scraper executing with %s processes", thread_count)
		self.thread_count = thread_count

	def start_aggregator(self):

		self.agg_proc = multiprocessing.Process(target=UpdateAggregator.launch_agg, args=(self.agg_queue, ))
		self.agg_proc.start()

	def join_aggregator(self):

		self.log.info("Asking Aggregator process to stop.")
		runStatus.agg_run_state.value = 0
		self.agg_proc.join(0)
		self.log.info("Aggregator joined.")

	def run(self):

		tasks =[]
		cnt = 10
		procno = 0

		self.start_aggregator()


		if self.thread_count == 1:
			self.log.info("Running in single process mode!")
			try:
				RunInstance.run(procno, self.agg_queue, cookie_lock=COOKIE_LOCK, job_get_lock=JOB_GET_LOCK, nosig=False)
			except KeyboardInterrupt:
				runStatus.run_state.value = 0


		elif self.thread_count < 1:
			self.log.error("Wat?")
		elif self.thread_count > 1:
			try:
				while runStatus.run_state.value:
					time.sleep(1)

					cnt += 1
					if cnt >= 10:
						cnt = 0
						living = sum([task.is_alive() for task in tasks])
						for dummy_x in range(self.thread_count - living):
							self.log.warning("Insufficent living child threads! Creating another thread with number %s", procno)
							proc = multiprocessing.Process(target=RunInstance.run, args=(procno, self.agg_queue), kwargs={'cookie_lock':COOKIE_LOCK, 'job_get_lock':JOB_GET_LOCK})
							tasks.append(proc)
							proc.start()
							procno += 1
						self.log.info("Living processes: %s", living)


						clean_tasks = []
						cleaned_count = len(tasks)
						for task in tasks:
							if not task.is_alive():
								task.join()
							else:
								clean_tasks.append(task)
						tasks = clean_tasks
						cleaned_count -= len(tasks)
						if cleaned_count > 0:
							self.log.warning("Run manager cleared out %s exited task instances.", cleaned_count)



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

