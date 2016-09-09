
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


if __name__ == "__main__":
	logSetup.initLogging()

import runStatus

import common.util.urlFuncs as urlFuncs
import RawArchiver.RawEngine
import RawArchiver.RawNewJobQueue as njq


import common.stuck
import common.database

NO_PROCESSES = 4
# NO_PROCESSES = 12
# NO_PROCESSES = 8
# NO_PROCESSES = 4
# NO_PROCESSES = 2
# NO_PROCESSES = 1


def initializeRawStartUrls(rules):
	print("Initializing all start URLs in the database")
	sess = common.database.get_db_session()
	for ruleset in [rset for rset in rules if rset['starturls']]:
		for starturl in ruleset['starturls']:
			have = sess.query(common.database.RawWebPages) \
				.filter(common.database.RawWebPages.url == starturl)   \
				.count()
			if not have:
				netloc = urlFuncs.getNetLoc(starturl)
				new = common.database.RawWebPages(
						url               = starturl,
						starturl          = starturl,
						netloc            = netloc,
						type              = ruleset['type'],
						priority          = common.database.DB_IDLE_PRIORITY,
						distance          = common.database.DB_DEFAULT_DIST,
						normal_fetch_mode = ruleset['normal_fetch_mode'],
					)
				print("Missing start-url for address: '{}'".format(starturl))
				sess.add(new)
			try:
				sess.commit()
			except Exception:
				print("Failure inserting start url for address: '{}'".format(starturl))

				sess.rollback()
	sess.close()
	common.database.delete_db_session()


def resetInProgress():
	print("Resetting any stalled downloads from the previous session.")

	sess = common.database.get_db_session()
	sess.query(common.database.RawWebPages) \
		.filter(
				(common.database.RawWebPages.state == "fetching")           |
				(common.database.RawWebPages.state == "processing")
				)   \
		.update({common.database.RawWebPages.state : "new"})
	sess.commit()
	sess.close()
	common.database.delete_db_session()


class RawRunInstance(object):
	def __init__(self, num, response_queue, new_job_queue, cookie_lock, nosig=True):
		# print("RawRunInstance %s init!" % num)
		if nosig:
			# signal.signal(signal.SIGINT, handler)
			signal.signal(signal.SIGINT, signal.SIG_IGN)
		self.num = num
		self.log = logging.getLogger("Main.Text.Web")
		self.resp_queue    = response_queue
		self.cookie_lock   = cookie_lock
		self.new_job_queue = new_job_queue

		# print("RawRunInstance %s MOAR init!" % num)

	def __del__(self):
		common.database.delete_db_session()

	def do_task(self):

		db_handle = common.database.get_db_session()

		hadjob = False
		try:
			self.archiver = RawArchiver.RawEngine.RawSiteArchiver(cookie_lock=self.cookie_lock, new_job_queue=self.new_job_queue, response_queue=self.resp_queue, db_interface=db_handle)
			hadjob = self.archiver.taskProcess()
		finally:
			# Clear out the sqlalchemy state
			db_handle.expunge_all()
			common.database.delete_db_session()

		return hadjob

	def go(self):

		self.log.info("RawRunInstance starting!")
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
		common.stuck.install_pystuck()

		try:
			run = cls(num, response_queue, new_job_queue, cookie_lock, nosig)
			# print("Class instantiated: ", run)
			run.go()
		except Exception:
			print()
			print("Exception in sub-process!")
			traceback.print_exc()


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
		mainManager    = MultiJobManager(max_tasks=self.thread_count, target=RawRunInstance.run, target_kwargs=kwargs)

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

