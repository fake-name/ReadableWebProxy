#!flask/bin/python

import sys
import os.path
import logging

os.environ['NDSCHEDULER_SETTINGS_MODULE'] = 'settings_sched'
addpath = os.path.abspath("./ndscheduler")
if addpath not in sys.path:
	sys.path.append(os.path.abspath("./ndscheduler"))

import traceback
import datetime
import threading
import time
import apscheduler.events
import apscheduler.triggers.interval
import apscheduler.triggers.cron

# Shut up fucking annoying psycopg2 vomit every exec.
import warnings
from sqlalchemy import exc as sa_exc
warnings.filterwarnings("ignore", category=UserWarning, module='psycopg2')
warnings.simplefilter("ignore", category=sa_exc.SAWarning)

import ndscheduler
import ndscheduler.server.server
import common.stuck
import activeScheduledTasks


JOB_MAP = {
		apscheduler.events.EVENT_SCHEDULER_STARTED  : "EVENT_SCHEDULER_STARTED",
		apscheduler.events.EVENT_SCHEDULER_SHUTDOWN : "EVENT_SCHEDULER_SHUTDOWN",
		apscheduler.events.EVENT_SCHEDULER_PAUSED   : "EVENT_SCHEDULER_PAUSED",
		apscheduler.events.EVENT_SCHEDULER_RESUMED  : "EVENT_SCHEDULER_RESUMED",
		apscheduler.events.EVENT_EXECUTOR_ADDED     : "EVENT_EXECUTOR_ADDED",
		apscheduler.events.EVENT_EXECUTOR_REMOVED   : "EVENT_EXECUTOR_REMOVED",
		apscheduler.events.EVENT_JOBSTORE_ADDED     : "EVENT_JOBSTORE_ADDED",
		apscheduler.events.EVENT_JOBSTORE_REMOVED   : "EVENT_JOBSTORE_REMOVED",
		apscheduler.events.EVENT_ALL_JOBS_REMOVED   : "EVENT_ALL_JOBS_REMOVED",
		apscheduler.events.EVENT_JOB_ADDED          : "EVENT_JOB_ADDED",
		apscheduler.events.EVENT_JOB_REMOVED        : "EVENT_JOB_REMOVED",
		apscheduler.events.EVENT_JOB_MODIFIED       : "EVENT_JOB_MODIFIED",
		apscheduler.events.EVENT_JOB_SUBMITTED      : "EVENT_JOB_SUBMITTED",
		apscheduler.events.EVENT_JOB_MAX_INSTANCES  : "EVENT_JOB_MAX_INSTANCES",
		apscheduler.events.EVENT_JOB_EXECUTED       : "EVENT_JOB_EXECUTED",
		apscheduler.events.EVENT_JOB_ERROR          : "EVENT_JOB_ERROR",
		apscheduler.events.EVENT_JOB_MISSED         : "EVENT_JOB_MISSED",
		apscheduler.events.EVENT_ALL                : "EVENT_ALL",
	}


log = logging.getLogger("Main.Runtime")

def job_evt_listener(event):
	if hasattr(event, "exception") and event.exception:
		log.info('Job crashed: %s', event.job_id)
		log.info('Traceback: %s', event.traceback)
	else:
		log.info('Job event code: %s, job: %s', JOB_MAP[event.code], event.job_id)
	if event.code == apscheduler.events.EVENT_JOB_MAX_INSTANCES:

		log.info('Job event code: %s, job: %s', JOB_MAP[event.code], event.job_id)
		log.error("Missed job execution! Killing job executor to unstick jobs")


		print('Job event code: %s, job: %s' % (JOB_MAP[event.code], event.job_id))
		print("Missed job execution! Killing job executor to unstick jobs")

		import ctypes
		ctypes.string_at(1)
		import os
		os.kill(0,4)

class SimpleServer(ndscheduler.server.server.SchedulerServer):

	def post_scheduler_start(self):
		active_jobs = set()
		current_jobs = self.scheduler_manager.get_jobs()

		# import pdb
		# pdb.set_trace()

		start_date = datetime.datetime.now()

		for job in current_jobs:
			job_str, job_id = job.args[:2]
			active_jobs.add(job_str)

			# We only actively manage jobs that start with "AUTO". That lets us
			# have manually added jobs that exist outside of the management interface.
			if not job.name.startswith("AUTO: "):
				continue

			if job_str not in activeScheduledTasks.target_jobs:
				print("Removing job: %s -> %s" % (job_str, job_id))
				self.scheduler_manager.remove_job(job_id)

			else:
				job_params = activeScheduledTasks.target_jobs[job_str]
				if job_params.get('interval'):
					trig = apscheduler.triggers.interval.IntervalTrigger(
							seconds    = job_params.get('interval'),
							start_date = start_date,
						)
					start_date = start_date + datetime.timedelta(minutes=5)
				else:
					trig = apscheduler.triggers.cron.CronTrigger(
							month       = job_params.get('month', None),
							day         = job_params.get('day', None),
							day_of_week = job_params.get('day_of_week', None),
							hour        = job_params.get('hour', None),
							minute      = job_params.get('minute', None),
						)

				if job.name != job_params['name']:
					self.scheduler_manager.remove_job(job_id)

				# So the apscheduler CronTrigger class doesn't provide the equality
				# operator, so we compare the stringified version. Gah.
				elif str(job.trigger) != str(trig):
					print("Removing trigger:", str(job.trigger), str(trig))
					self.scheduler_manager.remove_job(job_id)


		start_date = datetime.datetime.now()

		current_jobs = self.scheduler_manager.get_jobs()
		for job_name, params in activeScheduledTasks.target_jobs.items():
			if job_name not in active_jobs:
				assert params['name'].startswith("AUTO: ")
				print("Adding job: %s" % job_name)

				if params.get('interval'):
					trig = apscheduler.triggers.interval.IntervalTrigger(
							seconds    = params.get('interval'),
							start_date = start_date,
						)
					start_date = start_date + datetime.timedelta(minutes=5)
				else:
					trig = apscheduler.triggers.cron.CronTrigger(
							month       = params.get('month', None),
							day         = params.get('day', None),
							day_of_week = params.get('day_of_week', None),
							hour        = params.get('hour', None),
							minute      = params.get('minute', None),
						)

				self.scheduler_manager.add_trigger_job(
						job_class_string = job_name,
						name             = params['name'],
						trigger          = trig,
					)

		self.scheduler_manager.sched.add_listener(job_evt_listener,
				apscheduler.events.EVENT_JOB_EXECUTED |
				apscheduler.events.EVENT_JOB_ERROR    |
				apscheduler.events.EVENT_JOB_MISSED   |
				apscheduler.events.EVENT_JOB_MAX_INSTANCES
			)


def run_scheduler():
	common.stuck.install_pystuck()
	SimpleServer.run()


if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()
	run_scheduler()

