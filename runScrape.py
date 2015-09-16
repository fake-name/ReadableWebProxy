#!flask/bin/python

if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()

import WebMirror.Runner
import WebMirror.rules
import traceback
import datetime
import config
import WebMirror.database as db
import WebMirror.LogBase as LogBase
import sqlalchemy.exc

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ProcessPoolExecutor
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
	'main_jobstore'      : SQLAlchemyJobStore(url=SQLALCHEMY_DATABASE_URI)

}


CALLABLE_LUT = {}
for item, dummy_interval in activePlugins.scrapePlugins.values():
	CALLABLE_LUT[item.__name__] = item


class JobCaller(LogBase.LoggerMixin):

	loggerPath = "Main.PluginRunner"

	def __init__(self, job_name):

		if not job_name in CALLABLE_LUT:
			raise ValueError("Callable '%s' is not in the class lookup table: '%s'!" % (job_name, CALLABLE_LUT))
		self.runModule = CALLABLE_LUT[job_name]
		self.job_name = job_name

		session = db.get_session()

		try:
			query = session.query(db.PluginStatus).filter(db.PluginStatus.plugin_name==job_name)
			have = query.scalar()
			if not have:
				new = db.PluginStatus(plugin_name=job_name)
				session.add(new)
				session.commit()
		except sqlalchemy.exc.OperationalError:
			session.rollback()
		except sqlalchemy.exc.InvalidRequestError:
			session.rollback()

	def doCall(self):

		session = db.get_session()
		item = session.query(db.PluginStatus).filter(db.PluginStatus.plugin_name==self.job_name).one()
		if item.is_running:
			session.commit()
			self.log.error("Plugin %s is already running! Not doing re-entrant call!", self.job_name)
			return

		item.is_running = True
		item.last_run = datetime.datetime.now()
		session.commit()

		try:
			self._doCall()
		except Exception:
			item.last_error      = datetime.datetime.now()
			item.last_error_msg  = traceback.format_exc()
			raise
		finally:
			item.is_running = False
			item.last_run_end = datetime.datetime.now()
			session.commit()


	# Should probably be a lambda? Laaaazy.
	def _doCall(self):
		instance = self.runModule()
		instance._go()

	@classmethod
	def callMod(cls, passMod):
		mod = cls(passMod)
		mod.doCall()

def do_call(job_name):
	caller = JobCaller(job_name)
	caller.doCall()

def scheduleJobs(sched, timeToStart):

	jobs = []
	offset = 0
	for key, value in activePlugins.scrapePlugins.items():
		baseModule, interval = value
		jobs.append((key, baseModule, interval, timeToStart+datetime.timedelta(seconds=60*offset)))
		offset += 1

	activeJobs = []

	print("JobCaller: ", JobCaller)
	print("JobCaller.callMod: ", JobCaller.callMod)

	for jobId, callee, interval, startWhen in jobs:
		jId = callee.__name__
		print("JobID = ", jId)
		activeJobs.append(jId)
		if not sched.get_job(jId):


			sched.add_job(do_call,
						args=(callee.__name__, ),
						trigger='interval',
						seconds=interval,
						start_date=startWhen,
						id=jId,
						replace_existing=True,
						jobstore="main_jobstore",
						misfire_grace_time=2**30)


	for job in sched.get_jobs('main_jobstore'):
		if not job.id in activeJobs:
			sched.remove_job(job.id, 'main_jobstore')


def go():

	rules = WebMirror.rules.load_rules()
	WebMirror.Runner.initializeStartUrls(rules)
	WebMirror.Runner.resetInProgress()

	sched = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)

	startTime = datetime.datetime.now()+datetime.timedelta(seconds=10)
	scheduleJobs(sched, startTime)
	sched.start()


	runner = WebMirror.Runner.Crawler()
	runner.run()

	# print("Thread halted. App exiting.")

def profile():
	import cProfile
	import pstats
	cProfile.run('go()', "run.stats")
	p = pstats.Stats("run.stats")
	p.sort_stats('cumulative')
	p.print_stats(250)

if __name__ == "__main__":
	started = False
	if not started:
		started = True

		# profile()
		go()
