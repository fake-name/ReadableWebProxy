
import runStatus
import logSetup
import logging

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

if '__pypy__' in sys.builtin_module_names:
	import psycopg2cffi as psycopg2
else:
	import psycopg2


if __name__ == "__main__":
	logSetup.initLogging()

import config
import runStatus

import WebMirror.Engine
import WebMirror.rules
import common.util.urlFuncs as urlFuncs
import common.database as db
import WebMirror.JobDispatcher
import WebMirror.UrlUpserter
import RawArchiver.RawJobDispatcher

import RawArchiver.RawRunner
import WebMirror.Runner


class MultiJobManager(object):
	def __init__(self, max_tasks, target, target_args=None, target_kwargs=None):
		self.max_tasks     = max_tasks
		self.target        = target
		self.target_args   = target_args   if target_args   else ()
		self.target_kwargs = target_kwargs if target_kwargs else {}

		self.procno        = 0

		self.log = logging.getLogger("Main.Job.Launcher")

		self.tasklist = {}
		for x in range(max_tasks):
			self.tasklist[x] = None

	def check_run_jobs(self):
		print(("Tasklist: ", self.tasklist))

		living = sum([task.is_alive() for task in self.tasklist.values() if task])
		dead = []

		for x in range(self.max_tasks):
			self.log.info("Checking runstate of %s -> %s", x, self.tasklist[x] and self.tasklist[x].is_alive())
			if not self.tasklist[x] or not self.tasklist[x].is_alive():
				self.log.info("Thread %s appears to not be alive!", x)
				self.log.warning("Insufficent living child threads! Creating another thread with number %s", self.procno)
				self.log.info("Target func: %s", self.target)

				if self.tasklist[x]:
					dead.append(self.tasklist[x])

				args = (self.procno, )
				kwargs = self.target_kwargs
				kwargs['total_worker_count'] = self.max_tasks
				kwargs['worker_num']         = x

				if self.target_args:
					args += self.target_args
				with logSetup.stdout_lock:
					proc = multiprocessing.Process(target=self.target, args=args, kwargs=kwargs)
					# proc = threading.Thread(target=self.target, args=(self.procno, ) + self.target_args, kwargs=self.target_kwargs)
					proc.start()
					while not (                          # Wait until
								proc.is_alive()          # the process is running
							or  proc.exitcode != None):  # or has exited
						time.sleep(0.25)
						self.log.info("Waiting for process to start!")

					self.tasklist[x] = proc
					self.procno += 1


		cleaned = 0
		for dead_task in dead:
			dead_task.join()
			cleaned += 1

		if cleaned > 0:
			self.log.warning("Run manager cleared out %s exited task instances.", cleaned)

		return len(self.tasklist)

	def join_jobs(self, flushqueues):

		self.log.info("Run manager waiting on tasks to exit. Runstate = %s", runStatus.run_state.value)
		while 1:
			living = sum([task and task.is_alive() for task in self.tasklist.values()])
			self.log.info("Living processes: '%s'", living)

			for task in self.tasklist:
				task.join(3.0/(living+1))

			for job_queue in flushqueues:
					try:
						while 1:
							job_queue.get_nowait()
					except queue.Empty:
						pass

			living = sum([task and task.is_alive() for task in self.tasklist.values()])
			if living == 0:
				break

class Crawler(object):
	def __init__(self, main_thread_count, raw_thread_count):

		self.process_lookup = {}

		self.log = logging.getLogger("Main.Text.Manager")
		WebMirror.rules.load_rules()


		self.log.info("Scraper executing with %s main processes, %s raw scraper threads.", main_thread_count, raw_thread_count)
		self.main_thread_count = main_thread_count
		self.raw_thread_count = raw_thread_count

	def start_aggregator(self):
		agg_queue = multiprocessing.Queue()
		with logSetup.stdout_lock:
			self.main_job_agg = multiprocessing.Process(target=WebMirror.UrlUpserter.UpdateAggregator.launch_agg, args=(agg_queue, ))
			self.main_job_agg.start()
		return agg_queue

	def join_aggregator(self):

		self.log.info("Asking Aggregator process to stop.")
		runStatus.agg_run_state.value = 0
		if hasattr(self, 'main_job_agg'):
			self.main_job_agg.join(0)
		self.log.info("Aggregator joined.")

	def start_main_job_fetcher(self):

		self.main_job_fetcher = WebMirror.JobDispatcher.RpcJobManagerWrapper()
		return self.main_job_fetcher.get_queues()

	def start_raw_job_fetcher(self):
		self.raw_job_fetcher = RawArchiver.RawJobDispatcher.RawJobFetcher()
		return self.raw_job_fetcher.get_queue()

	def join_job_fetcher(self):
		self.log.info("Asking main job source task to halt.")
		if hasattr(self, 'main_job_fetcher'):
			self.main_job_fetcher.join_proc()
		self.log.info("Asking raw job source task to halt.")
		if hasattr(self, 'raw_job_fetcher'):
			self.raw_job_fetcher.join_proc()
		self.log.info("Job source halted.")

	def launchProcessesFromQueue(self, processes, job_in_queue):
		pass

	def run_raw(self):

		assert self.main_thread_count >= 1
		assert self.raw_thread_count >= 1

		# Dummy queues to shut up the teardown garbage
		new_url_aggreator_queue = queue.Queue()
		raw_new_job_queue       = self.start_raw_job_fetcher()

		raw_kwargs = {
			'response_queue' : new_url_aggreator_queue,
			'new_job_queue'  : raw_new_job_queue,
			'cookie_lock'    : runStatus.cookie_lock,
			}
		rawManager     = MultiJobManager(max_tasks=self.raw_thread_count, target=RawArchiver.RawRunner.RawRunInstance.run, target_kwargs=raw_kwargs)

		managers     = [rawManager]
		drain_queues = [raw_new_job_queue]
		flush_queues = [new_url_aggreator_queue, raw_new_job_queue]

		self._runloop(managers, drain_queues, flush_queues)

	def run(self):

		assert self.main_thread_count >= 1
		assert self.raw_thread_count >= 1

		new_url_aggreator_queue = self.start_aggregator()
		main_new_job_queue      = self.start_main_job_fetcher()
		# # cls, num, response_queue, new_job_queue, cookie_lock
		main_kwargs = {
			'response_queue' : new_url_aggreator_queue,
			'new_job_queue'  : main_new_job_queue,
			'cookie_lock'    : runStatus.cookie_lock,
			}
		mainManager    = MultiJobManager(max_tasks=self.main_thread_count, target=WebMirror.Runner.RunInstance.run, target_kwargs=main_kwargs)

		managers     = [mainManager]
		drain_queues = [main_new_job_queue]
		flush_queues = [new_url_aggreator_queue, main_new_job_queue]

		self._runloop(managers, drain_queues, flush_queues)

	def _runloop(self, managers, drain_queues, flush_queues):

		cnt = 10

		while runStatus.run_state.value:
			try:
				time.sleep(1)

				cnt += 1
				if cnt >= 10:
					cnt = 0

					living = sum([manager.check_run_jobs() for manager in managers])

					clok_locked = runStatus.cookie_lock.acquire(block=False)
					if clok_locked:
						runStatus.cookie_lock.release()

					self.log.info("Living processes: %s (Cookie lock acquired: %s, queue sizes: %s, exiting: %s)",
						living, not clok_locked, [q.qsize() for q in drain_queues], runStatus.run_state.value == 0)


			except KeyboardInterrupt:
				self.log.info("Control C caught. Stopping scraper.")
				break

			except Exception:
				print("Wat?")
				traceback.print_exc()
				with open("error %s.txt" % time.time(), "w") as fp:
					fp.write("Manager crashed?\n")
					fp.write(traceback.format_exc())
				break

		# Stop the job fetcher, and then let the active jobs
		# flush down.
		self.join_job_fetcher()

		runStatus.run_state.value = 0

		self.log.info("Crawler allowing ctrl+c to propagate.")
		time.sleep(1)
		runStatus.run_state.value = 0
		time.sleep(1)



		for manager in managers:
			manager.join_jobs(drain_queues)

		self.log.info("All processes halted.")

		self.log.info("Flusing queues")

		for job_queue in flush_queues:
			try:
				while 1:
					job_queue.get_nowait()
			except queue.Empty:
				pass

		self.join_aggregator()


