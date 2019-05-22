#!flask/bin/python

import sys
import os
import os.path

os.environ['NDSCHEDULER_SETTINGS_MODULE'] = 'settings_sched'

sys.path.append(os.path.abspath("./ndscheduler"))

import traceback
import datetime
import threading
import time
import apscheduler.triggers.cron

# Shut up fucking annoying psycopg2 vomit every exec.
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='psycopg2')



import ndscheduler
import ndscheduler.server.server


target_jobs = {

	'scheduled_jobs.python_job.RssTriggerJob' : {
		"name"             : 'AUTO: Rss Feeds Trigger job',
		"minute"           : '*/42',
	},
	'scheduled_jobs.python_job.RollingRewalkTriggersBaseJob' : {
		"name"             : 'AUTO: Rolling Rewalk Trigger job',
		"minute"           : '15',
		"hour"             : '*/4',
	},
	'scheduled_jobs.python_job.HourlyPageTriggerJob' : {
		"name"             : 'AUTO: Hourly Page Trigger job',
		"minute"           : '0',
		"hour"             : '*',
	},
	'scheduled_jobs.python_job.EverySixHoursPageTriggerJob' : {
		"name"             : 'AUTO: Every Six Hours Trigger job',
		"minute"           : '45',
		"hour"             : '*/6',
	},
	'scheduled_jobs.python_job.EveryOtherDayPageTriggerJob' : {
		"name"             : 'AUTO: Every other day Trigger job',
		"day"              : '*/2',
		"minute"           : '30',
		"hour"             : '15',
	},
	'scheduled_jobs.python_job.NuQueueTriggerJob' : {
		"name"             : 'AUTO: NU Homepage Fetch',
		"minute"           : '*/40',
	},
	'scheduled_jobs.python_job.HourlyLocalFetchTriggerJob' : {
		"name"             : 'AUTO: Hourly local fetch trigger job',
		"minute"           : '0',
	},
	'scheduled_jobs.python_job.DbFlattenerJob' : {
		"name"             : 'AUTO: DB Flattener job',
		"day"              : '*/3',
		"minute"           : '30',
		"hour"             : '5',
	},
	'scheduled_jobs.python_job.RssFunctionSaverJob' : {
		"name"             : 'AUTO: Function Saver job',
		"minute"           : '50',
		"hour"             : '*/12',
	},
	'scheduled_jobs.python_job.TransactionTruncatorJob' : {
		"name"             : 'AUTO: Transaction table truncator job',
		"minute"           : '*/25',
	},
	'scheduled_jobs.python_job.RollingRawRewalkTriggerJob' : {
		"name"             : 'AUTO: Rolling Raw Rewalk Trigger job',
		"minute"           : '10',
		"hour"             : '*/12',
	},
	'scheduled_jobs.python_job.NuHeaderJob' : {
		"name"             : 'AUTO: NuHeader job',
		"minute"           : '*/22',
		"hour"             : '*',
	},


}


class SimpleServer(ndscheduler.server.server.SchedulerServer):

	def post_scheduler_start(self):
		# New user experience! Make sure we have at least 1 job to demo!

		active_jobs = set()
		current_jobs = self.scheduler_manager.get_jobs()

		# import pdb
		# pdb.set_trace()

		for job in current_jobs:
			job_str, job_id = job.args
			active_jobs.add(job_str)

			# We only actively manage jobs that start with "AUTO". That lets us
			# have manually added jobs that exist outside of the management interface.
			if not job.name.startswith("AUTO: "):
				continue

			if job_str not in target_jobs:
				print("Removing job: %s -> %s" % (job_str, job_id))
				self.scheduler_manager.remove_job(job_id)

			else:
				job_params = target_jobs[job_str]
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
					self.scheduler_manager.remove_job(job_id)


		current_jobs = self.scheduler_manager.get_jobs()
		for job_name, params in target_jobs.items():
			if job_name not in active_jobs:
				assert params['name'].startswith("AUTO: ")
				print("Adding job: %s" % job_name)
				self.scheduler_manager.add_job(
						job_class_string = job_name,
						name             = params['name'],
						month            = params.get('month', None),
						day_of_week      = params.get('day_of_week', None),
						minute           = params.get('minute', None),
						hour             = params.get('hour', None),
						day              = params.get('day', None),
					)


def run_scheduler():
	SimpleServer.run()


if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()
	run_scheduler()

