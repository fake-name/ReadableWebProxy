
import time
import os
import multiprocessing
import signal
import logging
import logSetup
import cProfile
import traceback
import threading
import sys
import queue

# from pympler.tracker import SummaryTracker, summary, muppy
# import tracemalloc

import sqlalchemy.exc
from sqlalchemy.sql import text
from sqlalchemy.sql import func
import psycopg2


if __name__ == "__main__":
	logSetup.initLogging()

import config
import runStatus

import WebMirror.Engine
import WebMirror.OutputFilters.AmqpInterface
import WebMirror.rules
import common.util.urlFuncs as urlFuncs
import common.database as db
import WebMirror.NewJobQueue as njq

NO_PROCESSES = 24
# NO_PROCESSES = 12
# NO_PROCESSES = 8
# NO_PROCESSES = 4
# NO_PROCESSES = 2
# NO_PROCESSES = 1

# For synchronizing saving cookies to disk
COOKIE_LOCK  = multiprocessing.Lock()


def install_pystuck():
	import pystuck
	stuck_port = 6666
	while 1:
		try:
			pystuck.run_server(port=stuck_port)
			print("PyStuck installed to process, running on port %s" % stuck_port)
			return
		except OSError:
			stuck_port += 1
		if stuck_port > 7000:
			raise RuntimeError("wat?")

def halt_exc(x, y):
	if runStatus.run_state.value == 0:
		print("Raising Keyboard Interrupt")
		raise KeyboardInterrupt

def handler(signum, frame):
	for th in threading.enumerate():
		print("Dumping stack for thread: ", th)
		traceback.print_stack(sys._current_frames()[th.ident])
		print()

class RunInstance(object):
	def __init__(self, num, response_queue, new_job_queue, cookie_lock, nosig=True):
		# print("RunInstance %s init!" % num)
		if nosig:
			# signal.signal(signal.SIGINT, handler)
			signal.signal(signal.SIGINT, signal.SIG_IGN)
		self.num = num
		self.log = logging.getLogger("Main.Text.Web")
		self.resp_queue    = response_queue
		self.cookie_lock   = cookie_lock
		self.new_job_queue = new_job_queue

		# print("RunInstance %s MOAR init!" % num)

	def __del__(self):
		db.delete_db_session()

	def do_task(self):

		db_handle = db.get_db_session()

		hadjob = False
		try:
			self.archiver = WebMirror.Engine.SiteArchiver(self.cookie_lock, new_job_queue=self.new_job_queue, response_queue=self.resp_queue, db_interface=db_handle)
			hadjob = self.archiver.taskProcess()
		finally:
			# Clear out the sqlalchemy state
			db_handle.expunge_all()
			db.delete_db_session()

		return hadjob

	def go(self):

		self.log.info("RunInstance starting!")
		loop = 0
		# We have to only let the child threads run for a period of time, or something
		# somewhere in sqlalchemy appears to be leaking memory.
		for dummy_x in range(100):

			if runStatus.run_state.value == 1:
				# objgraph.show_growth(limit=3)
				hadjob = self.do_task()
			else:
				self.log.info("Thread %s exiting.", self.num)
				break
			loop += 1

			# If there was nothing to do, sleep 30 seconds and recheck.
			# This is because with 50 workers with a sleep-time of 5 seconds on job-miss,
			# it was causing 100% CPU usage on the DB just for the getjob queries. (I think)
			if not hadjob:
				sleeptime = 10
				self.log.info("Nothing for thread %s to do. Sleeping %s seconds.", self.num, sleeptime)
				for _x in range(sleeptime):
					time.sleep(1)
					if runStatus.run_state.value != 1:
						self.log.info("Thread %s saw exit flag while waiting for jobs. Runstate: %s", self.num, runStatus.run_state.value)
						return

		if runStatus.run_state.value:
			self.log.info("Thread %s restarting. Runstate: %s", self.num, runStatus.run_state.value)
		else:
			self.log.info("Thread %s halting. Runstate: %s", self.num, runStatus.run_state.value)




	@classmethod
	def run_prof(cls, num, response_queue, new_job_queue, cookie_lock, nosig=True):

		pid = os.getpid()
		try:
			cProfile.runctx('cls.run(num, response_queue, new_job_queue, cookie_lock, nosig)', globals(), locals(), 'prof%d.prof' % pid)
		except Exception as e:
			print("Wat?")
			print("Wat?")
			print("Wat?")
			print("Wat?")
			print("Wat?")
			print("Wat?")
			print("Wat?")
			traceback.print_exc()
			raise e

	@classmethod
	def run(cls, num, response_queue, new_job_queue, cookie_lock, nosig=True):
		logSetup.resetLoggingLocks()
		install_pystuck()

		try:
			run = cls(num, response_queue, new_job_queue, cookie_lock, nosig)
			# print("Class instantiated: ", run)
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
			try:
				sess.commit()
			except sqlalchemy.SQLAlchemyError:
				print("Failure inserting start url for address: '{}'".format(starturl))

				sess.rollback()
	sess.close()
	db.delete_db_session()

def resetInProgress():
	print("Resetting any stalled downloads from the previous session.")

	sess = db.get_db_session()
	sess.query(db.WebPages) \
		.filter(
				(db.WebPages.state == "fetching")           |
				(db.WebPages.state == "processing")         |
				(db.WebPages.state == "specialty_deferred") |
				(db.WebPages.state == "specialty_ready")
				)   \
		.update({db.WebPages.state : "new"})
	sess.commit()
	sess.close()
	db.delete_db_session()

class UpdateAggregator(object):
	def __init__(self, msg_queue, db_interface):
		self.queue = msg_queue
		self.log = logging.getLogger("Main.Agg.Manager")

		amqp_settings = {
			"RABBIT_LOGIN"   : config.C_RABBIT_LOGIN,
			"RABBIT_PASWD"   : config.C_RABBIT_PASWD,
			"RABBIT_SRVER"   : config.C_RABBIT_SRVER,
			"RABBIT_VHOST"   : config.C_RABBIT_VHOST,
			'taskq_task'     : 'task.master.q',
			'taskq_response' : 'response.master.q',
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


		raw_cur = self.db_int.connection().connection.cursor()

		#  Fucking huzzah for ON CONFLICT!
		cmd = """
				INSERT INTO
					web_pages
					(url, starturl, netloc, distance, is_text, priority, type, addtime, state)
				VALUES
					(%(url)s, %(starturl)s, %(netloc)s, %(distance)s, %(is_text)s, %(priority)s, %(type)s, %(addtime)s, %(state)s)
				ON CONFLICT (url) DO
					UPDATE
						SET
							state           = EXCLUDED.state,
							starturl        = EXCLUDED.starturl,
							netloc          = EXCLUDED.netloc,
							is_text         = EXCLUDED.is_text,
							distance        = LEAST(EXCLUDED.distance, web_pages.distance),
							priority        = GREATEST(EXCLUDED.priority, web_pages.priority),
							addtime         = LEAST(EXCLUDED.addtime, web_pages.addtime)
						WHERE
						(
								web_pages.ignoreuntiltime < %(ignoreuntiltime)s
							AND
								web_pages.url = EXCLUDED.url
							AND
								(web_pages.state = 'complete' OR web_pages.state = 'error')
						)
					;
				""".replace("	", " ").replace("\n", " ")

		# Only commit per-URL if we're tried to do the update in batch, and failed.
		commit_each = False
		while 1:
			try:
				for paramset in self.batched_links:

					if len(paramset['url']) > 2000:
						self.log.error("URL Is too long to insert into the database!")
						self.log.error("URL: '%s'", paramset['url'])

					else:
						# Forward-data the next walk, time, rather then using now-value for the thresh.
						raw_cur.execute(cmd, paramset)
						if commit_each:
							raw_cur.execute("COMMIT;")

				raw_cur.execute("COMMIT;")
				break

			except psycopg2.Error:
				if commit_each is False:
					self.log.warning("psycopg2.Error - Retrying with commit each.")
				else:
					self.log.warning("psycopg2.Error - Retrying.")
					traceback.print_exc()

				raw_cur.execute("ROLLBACK;")
				commit_each = True


		self.batched_links = []




		# while 1:
		# 	try:

		# 		cmd = text("""
		# 				INSERT INTO
		# 					web_pages
		# 					(url, starturl, netloc, distance, is_text, priority, type, addtime, state)
		# 				VALUES
		# 					(%(url)s, %(starturl)s, %(netloc)s, %(distance)s, %(is_text)s, %(priority)s, %(type)s, %(addtime)s, %(state)s)
		# 				ON CONFLICT (url) DO
		# 					UPDATE
		# 						SET
		# 							state           = EXCLUDED.state,
		# 							starturl        = EXCLUDED.starturl,
		# 							netloc          = EXCLUDED.netloc,
		# 							is_text         = EXCLUDED.is_text,
		# 							distance        = LEAST(EXCLUDED.distance, web_pages.distance),
		# 							priority        = GREATEST(EXCLUDED.priority, web_pages.priority),
		# 							addtime         = LEAST(EXCLUDED.addtime, web_pages.addtime)
		# 						WHERE
		# 						(
		# 								web_pages.ignoreuntiltime < %(ignoreuntiltime)s
		# 							AND
		# 								web_pages.url = EXCLUDED.url
		# 							AND
		# 								(web_pages.state = 'complete' OR web_pages.state = 'error')
		# 						)
		# 					;
		# 				""".replace("	", " ").replace("\n", " "))


		# 		# cmd = text("""
		# 		# 		INSERT INTO
		# 		# 			web_pages
		# 		# 			(url, starturl, netloc, distance, is_text, priority, type, fetchtime, state)
		# 		# 		VALUES
		# 		# 			(:url, :starturl, :netloc, :distance, :is_text, :priority, :type, :fetchtime, :state)
		# 		# 		ON CONFLICT DO NOTHING
		# 		# 		""")

		# 		for paramset in self.batched_links:
		# 			self.db_int.execute(cmd, params=paramset)
		# 		self.db_int.commit()
		# 		self.batched_links = []
		# 		break
		# 	except KeyboardInterrupt:
		# 		self.log.info("Keyboard Interrupt?")
		# 		self.db_int.rollback()
		# 	except sqlalchemy.exc.InternalError:
		# 		self.log.info("Transaction error. Retrying.")
		# 		traceback.print_exc()
		# 		self.db_int.rollback()
		# 	except sqlalchemy.exc.OperationalError:
		# 		self.log.info("Transaction error. Retrying.")
		# 		traceback.print_exc()
		# 		self.db_int.rollback()
		# self.db_int.close()


	def do_link(self, linkdict):

		assert 'url'             in linkdict
		assert 'starturl'        in linkdict
		assert 'netloc'          in linkdict
		assert 'distance'        in linkdict
		assert 'is_text'         in linkdict
		assert 'priority'        in linkdict
		assert 'type'            in linkdict
		assert 'state'           in linkdict
		assert 'addtime'         in linkdict
		assert 'ignoreuntiltime' in linkdict

		url = linkdict['url']

		if not url in self.seen:
			# Fucking huzzah for ON CONFLICT!
			self.batched_links.append(linkdict)
			self.seen[url] = time.time()

			if len(self.batched_links) > 100:
				self.do_link_batch_update()
		# 	print("Inserting", url, len(self.seen))
		# else:
		# 	print("Skipping", url)


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
				for line in traceback.format_exc().split("\n"):
					self.log.error(line.rstrip())

	def close(self):
		if config.C_DO_RABBIT:
			self.log.info("Aggregator thread closing interface.")
			self._amqpint.close()

	@classmethod
	def launch_agg(cls, agg_queue):
		install_pystuck()
		agg_db = db.get_db_session()
		instance = cls(agg_queue, agg_db)
		instance.run()
		instance.close()

class MultiJobManager(object):
	def __init__(self, max_tasks, target, target_args=None, target_kwargs=None):
		self.max_tasks     = max_tasks
		self.target        = target
		self.target_args   = target_args
		self.target_kwargs = target_kwargs

		self.procno        = 0

		self.log = logging.getLogger("Main.Job.Launcher")

		self.tasklist = []

	def check_run_jobs(self):

		living = sum([task.is_alive() for task in self.tasklist])
		for dummy_x in range(self.max_tasks - living):
			self.log.warning("Insufficent living child threads! Creating another thread with number %s", self.procno)
			with logSetup.stdout_lock:
				args = (self.procno, )
				if self.target_args:
					args += self.target_args
				proc = multiprocessing.Process(target=self.target, args=args, kwargs=self.target_kwargs)
				# proc = threading.Thread(target=self.target, args=(self.procno, ) + self.target_args, kwargs=self.target_kwargs)
				self.tasklist.append(proc)
				proc.start()
				self.procno += 1

		cleaned = 0
		for task in self.tasklist:
			if not task.is_alive():
				task.join()
				cleaned += 1

		if cleaned > 0:
			self.tasklist = [task for task in self.tasklist if task.is_alive()]
			self.log.warning("Run manager cleared out %s exited task instances.", cleaned)

		return len(self.tasklist)

	def join_jobs(self, flushqueues):

		self.log.info("Run manager waiting on tasks to exit. Runstate = %s", runStatus.run_state.value)
		while 1:
			living = sum([task.is_alive() for task in self.tasklist])
			for task in self.tasklist:
				task.join(3.0/(living+1))

			self.log.info("Living processes: '%s'", living)

			for job_queue in flushqueues:
					try:
						while 1:
							job_queue.get_nowait()
					except queue.Empty:
						pass

			if living == 0:
				break

class Crawler(object):
	def __init__(self, thread_count=NO_PROCESSES):

		self.process_lookup = {}

		self.log = logging.getLogger("Main.Text.Manager")
		WebMirror.rules.load_rules()


		self.log.info("Scraper executing with %s processes", thread_count)
		self.thread_count = thread_count

	def start_aggregator(self):
		agg_queue = multiprocessing.Queue()
		with logSetup.stdout_lock:
			self.agg_proc = multiprocessing.Process(target=UpdateAggregator.launch_agg, args=(agg_queue, ))
			self.agg_proc.start()
		return agg_queue

	def join_aggregator(self):

		self.log.info("Asking Aggregator process to stop.")
		runStatus.agg_run_state.value = 0
		self.agg_proc.join(0)
		self.log.info("Aggregator joined.")

	def start_job_fetcher(self):
		self.job_agg = njq.JobAggregator()


		return self.job_agg.get_queues()

	def join_job_fetcher(self):
		self.log.info("Asking Job source task to halt.")

		self.job_agg.join_proc()
		self.log.info("Job source halted.")

	def launchProcessesFromQueue(self, processes, job_in_queue):
		pass


	def run(self):

		cnt = 10

		new_url_aggreator_queue = self.start_aggregator()

		new_job_queue = self.start_job_fetcher()

		assert self.thread_count >= 1

		# cls, num, response_queue, new_job_queue, cookie_lock
		kwargs = {
			'response_queue' : new_url_aggreator_queue,
			'new_job_queue'  : new_job_queue,
			'cookie_lock'    : COOKIE_LOCK,
			}
		mainManager    = MultiJobManager(max_tasks=self.thread_count, target=RunInstance.run, target_kwargs=kwargs)

		managers = [mainManager]


		try:
			while runStatus.run_state.value:
				time.sleep(1)

				cnt += 1
				if cnt >= 10:
					cnt = 0

					living = sum([manager.check_run_jobs() for manager in managers])

					clok_locked = COOKIE_LOCK.acquire(block=False)
					if clok_locked:
						COOKIE_LOCK.release()

					self.log.info("Living processes: %s (Cookie lock acquired: %s, items in job queue: %s, exiting: %s)",
						living, not clok_locked, new_job_queue.qsize(), runStatus.run_state.value == 0)


		except KeyboardInterrupt:

			# Stop the job fetcher, and then let the active jobs
			# flush down.
			self.join_job_fetcher()

			runStatus.run_state.value = 0

			self.log.info("Crawler allowing ctrl+c to propagate.")
			time.sleep(1)
			runStatus.run_state.value = 0
			time.sleep(1)

			flushqueues = [new_job_queue, new_url_aggreator_queue]


			for manager in managers:
				manager.join_jobs(flushqueues)

			self.log.info("All processes halted.")

		self.log.info("Flusing queues")

		for job_queue in [new_job_queue, new_url_aggreator_queue]:
			try:
				while 1:
					job_queue.get_nowait()
			except queue.Empty:
				pass

		self.join_aggregator()



if __name__ == "__main__":
	runner = Crawler()
	runner.run()
	print(runner)

