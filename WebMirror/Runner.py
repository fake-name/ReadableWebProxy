
import time
import os
import signal
import logging
import cProfile
import traceback

import logSetup

import runStatus

import WebMirror.Engine
import WebMirror.rules

import common.database as db
import common.stuck
import Misc.install_vmprof


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

		# Shaddup, pylint
		self.archiver = None

	def __del__(self):
		db.delete_db_session()

	def do_task(self):

		db_handle = db.get_db_session()

		hadjob = False
		try:
			self.archiver = WebMirror.Engine.SiteArchiver(self.cookie_lock, new_job_queue=self.new_job_queue, response_queue=self.resp_queue, db_interface=db_handle)
			for x in range(500):
				hadjob = self.archiver.taskProcess()
				if not hadjob:
					return hadjob
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
		for dummy_x in range(500):

			if runStatus.run_state.value == 1:
				# objgraph.show_growth(limit=3)
				hadjob = self.do_task()
			else:
				self.log.info("Thread %s exiting.", self.num)
				break
			loop += 1

			# If there was nothing to do, sleep and recheck.
			if not hadjob:
				time.sleep(1)
				if runStatus.run_state.value != 1:
					self.log.info("Thread %s saw exit flag while waiting for jobs. Runstate: %s", self.num, runStatus.run_state.value)
					break

		if runStatus.run_state.value == 1:
			self.log.info("Thread %s Exited with a non-die runstate!. Runstate: %s", self.num, runStatus.run_state.value)
		else:
			self.log.info("Thread %s halting. Runstate: %s", self.num, runStatus.run_state.value)


	@classmethod
	def run_prof(cls, num, total_worker_count, worker_num, response_queue, new_job_queue, cookie_lock, nosig=True):

		logSetup.resetLoggingLocks()
		common.process.name_process("proc fetcher processing worker w-profiling")

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
	def run(cls, num, total_worker_count, worker_num, response_queue, new_job_queue, cookie_lock, nosig=True):
		logSetup.resetLoggingLocks()
		common.process.name_process("proc fetcher processing worker")


		# Misc.install_vmprof.install_vmprof("runner")

		# total_worker_count, worker_num are ignored at the moment.

		try:
			run = cls(num, response_queue, new_job_queue, cookie_lock, nosig)
			# print("Class instantiated: ", run)
			run.go()
		except Exception:
			print()
			print("Exception in sub-process!")
			traceback.print_exc()
		# finally:
		# 	Misc.install_vmprof.close_profile_file()
