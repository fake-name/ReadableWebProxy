#!flask/bin/python

if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()

import WebMirror.Runner
import WebMirror.rules
import sys
import datetime
import config

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

import activePlugins

executors = {
	'main_jobstore': ProcessPoolExecutor(10),
}
job_defaults = {
	'coalesce': True,
	'max_instances': 1
}

SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{passwd}@{host}:5432/{database}'.format(user=config.C_DATABASE_USER, passwd=config.C_DATABASE_PASS, host=config.C_DATABASE_IP, database=config.C_DATABASE_DB_NAME)

jobstores = {

	'transient_jobstore' : MemoryJobStore(),
	'main_jobstore'      : SQLAlchemyJobStore(url=SQLALCHEMY_DATABASE_URI)

}


# Should probably be a lambda? Laaaazy.
def callMod(passMod):
	lut = {}
	for item, dummy_interval in activePlugins.scrapePlugins.values():
		lut[item.__name__] = item
	if not passMod in lut:
		raise ValueError("Callable '%s' is not in the class lookup table: '%s'!" % (passMod, lut))
	runModule = lut[passMod]
	instance = runModule()
	instance._go()


def scheduleJobs(sched, timeToStart):

	jobs = []
	offset = 0
	for key, value in activePlugins.scrapePlugins.items():
		baseModule, interval = value
		jobs.append((key, baseModule, interval, timeToStart+datetime.timedelta(seconds=60*offset)))
		offset += 1

	activeJobs = []

	for jobId, callee, interval, startWhen in jobs:
		jId = callee.__name__
		activeJobs.append(jId)
		if not sched.get_job(jId):

			# Jobs that are called less often then once every 4 hours get placed
			# in the main jobstore.
			# More ephemeral jobs get stored in the memory jobstore.
			if interval < (60 * 60 * 4):
				jobstore = "transient_jobstore"
			else:
				jobstore = "main_jobstore"


			sched.add_job(callMod,
						args=(callee.__name__, ),
						trigger='interval',
						seconds=interval,
						start_date=startWhen,
						id=jId,
						replace_existing=True,
						jobstore=jobstore,
						misfire_grace_time=2**30)


	for job in sched.get_jobs('main_jobstore'):
		if not job.id in activeJobs:
			sched.remove_job(job.id, 'main_jobstore')


def go():

	rules = WebMirror.rules.load_rules()
	WebMirror.Runner.initializeStartUrls(rules)

	sched = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)

	# startTime = datetime.datetime.now()+datetime.timedelta(seconds=60*60)
	# startTime = datetime.datetime.now()+datetime.timedelta(seconds=60*15)
	# startTime = datetime.datetime.now()+datetime.timedelta(seconds=60*5)
	# startTime = datetime.datetime.now()+datetime.timedelta(seconds=20)
	startTime = datetime.datetime.now()+datetime.timedelta(seconds=10)
	scheduleJobs(sched, startTime)
	sched.start()


	runner = WebMirror.Runner.Crawler()
	runner.run()

	# print("Thread halted. App exiting.")

if __name__ == "__main__":
	started = False
	if not started:
		started = True
		go()
