#!flask/bin/python

if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()

import WebMirror.Runner
import WebMirror.rules
import sys
import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore

import activePlugins

executors = {
	'main_jobstore': ProcessPoolExecutor(20),
}
job_defaults = {
	'coalesce': True,
	'max_instances': 1
}

jobstores = {

	'main_jobstore' : MemoryJobStore(),

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
			sched.add_job(callMod,
						args=(callee.__name__, ),
						trigger='interval',
						seconds=interval,
						start_date=startWhen,
						id=jId,
						replace_existing=True,
						jobstore='main_jobstore',
						misfire_grace_time=2**30)




def go():
	if "init" in sys.argv:

		rules = WebMirror.rules.load_rules()
		WebMirror.Runner.initializeStartUrls(rules)
	else:

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
