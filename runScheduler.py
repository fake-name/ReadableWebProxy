#!flask/bin/python

import sys
import traceback
import datetime
import threading
import time
from pytz import reference
import pytz

import sqlalchemy.exc

from apscheduler.schedulers.blocking   import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool        import ProcessPoolExecutor
from apscheduler.executors.pool        import ThreadPoolExecutor
from apscheduler.jobstores.sqlalchemy  import SQLAlchemyJobStore

import config
import common.database as db
import common.LogBase as LogBase

if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()

from settings import NO_PROCESSES
from settings import MAX_DB_SESSIONS

from common.db_engine import SQLALCHEMY_DATABASE_URI
import activePlugins

CALLABLE_LUT = {}
for item, dummy_interval in activePlugins.scrapePlugins.values():
	print("Plugin: ", item.__name__)
	assert item.__name__ not in CALLABLE_LUT, "Plugin appears twice in call lookup table (%s)?" % item.__name__
	CALLABLE_LUT[item.__name__] = item


class JobNameException(Exception):
	pass

class JobCaller(LogBase.LoggerMixin):

	loggerPath = "Main.PluginRunner"

	def __init__(self, job_name):

		if not job_name in CALLABLE_LUT:
			raise JobNameException("Callable '%s' is not in the class lookup table: '%s'!" % (job_name, CALLABLE_LUT))
		self.runModule = CALLABLE_LUT[job_name]
		self.job_name = job_name


		session = db.get_db_session()

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

		finally:
			db.delete_db_session()

	def doCall(self):

		self.log.info("Calling job %s", self.job_name)
		session = db.get_db_session()
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

			item2 = session.query(db.PluginStatus).filter(db.PluginStatus.plugin_name==self.job_name).one()
			item2.is_running = False
			item2.last_run_end = datetime.datetime.now()
			session.commit()
			db.delete_db_session()
		self.log.info("Job %s complete.", self.job_name)

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

	while 1:
		try:
			caller.doCall()
			break
		except JobNameException:
			print("Error! Invalid job name: '%s'!" % job_name)
			break
		except AttributeError:
			traceback.print_exc()
			print("Call error!")



def scheduleJobs(sched, timeToStart):

	jobs = []
	offset = 0
	for key, value in activePlugins.scrapePlugins.items():
		baseModule, interval = value
		jobs.append((key, baseModule, interval, timeToStart+datetime.timedelta(seconds=60*offset)))
		offset += 1

	activeJobs = []


	for callable_f in activePlugins.autoscheduler_plugins:
		callable_f(sched)


	print("JobCaller: ", JobCaller)
	print("JobCaller.callMod: ", JobCaller.callMod)

	for jobId, callee, interval, startWhen in jobs:
		jId = callee.__name__
		activeJobs.append(jId)
		if sched.get_job(jId):
			print("JobID %s already scheduled." % jId)
		else:
			print("Need to add new job for ID: ", jId)
			sched.add_job(do_call,
						args               = (callee.__name__, ),
						trigger            = 'interval',
						# jobstore           = 'sqlalchemy',
						seconds            = interval,
						next_run_time      = startWhen,
						id                 = jId,
						replace_existing   = True,
						max_instances      = 5,
						coalesce           = True,
						misfire_grace_time = 2**30)


	for job in sched.get_jobs('main_jobstore'):
		if not job.id in activeJobs:
			print("Extra job in jobstore: %s. Removing." % job.id)
			sched.remove_job(job.id, 'main_jobstore')


def resetRunStates():
	print("JobSetup call resetting run-states!")
	session = db.get_db_session()
	session.query(db.PluginStatus).update({db.PluginStatus.is_running : False})
	session.commit()
	db.delete_db_session()
	print("Run-states reset.")


def dump_scheduled_jobs(sched):
	print("Scheduled jobs:")
	existing = sched.get_jobs()
	if not existing:
		print("	No jobs in scheduler!")

	tznow = datetime.datetime.now(tz=pytz.utc)
	for job in existing:
		print("	", job, job.args, "running in:", job.next_run_time - tznow)

	session = db.get_db_session()
	running = session.query(db.PluginStatus).filter(db.PluginStatus.is_running == True).all()
	print("Running jobs:")
	for jitem in running:
		print("	", jitem.plugin_name, jitem.is_running, jitem.last_run, jitem.last_error, jitem.last_error_msg)
	if not running:
		print("	<None!>")

	print("Running threads:")
	for thread in threading.enumerate():
		print("	", thread.getName(), thread)
	db.delete_db_session()


	# session = db.get_db_session()
	# items = session.query(db.PluginStatus).all()
	# print("Jobs in DB:")
	# for item in items:
	# 	print("	", item)
	# db.delete_db_session()


def go_sched():
	resetRunStates()

	sched = BackgroundScheduler({
			'apscheduler.jobstores.default': {
				'type': 'sqlalchemy',
				'url': SQLALCHEMY_DATABASE_URI
			},
			'apscheduler.jobstores.memory': {
				'type': 'memory'
			},
			# 'apscheduler.executors.default': {
			# 	'class': 'apscheduler.executors.pool:ProcessPoolExecutor',
			# 	'max_workers': '10'
			# },
			'apscheduler.executors.default': {
				'class': 'apscheduler.executors.pool:ThreadPoolExecutor',
				'max_workers': '10'
			},
			'apscheduler.job_defaults.coalesce': 'true',
			'apscheduler.job_defaults.max_instances': '5',
		})

	# Apparently the scheduler pull the jobs from the backend until you start it,
	# so if you're trying to validate the jobs already present, you have to start it
	# before iterating over jobs in the jobstore.
	sched.start()

	print("Jobs in scheduler:")
	dump_scheduled_jobs(sched)
	startTime = datetime.datetime.now(tz=pytz.utc)+datetime.timedelta(seconds=10)
	scheduleJobs(sched, startTime)
	dump_scheduled_jobs(sched)
	print("Starting scheduler.")
	while 1:
		try:
			dump_scheduled_jobs(sched)
			time.sleep(30)
		except KeyboardInterrupt:
			break
	sched.shutdown()


if __name__ == "__main__":

	print("Auxilliary modes: 'test', 'scheduler'.")


	largv = [tmp.lower() for tmp in sys.argv]

	global NO_PROCESSES
	global MAX_DB_SESSIONS

	MAX_DB_SESSIONS = NO_PROCESSES + 5
	MAX_DB_SESSIONS = 4
	go_sched()
