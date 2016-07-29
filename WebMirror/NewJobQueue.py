import sys
import multiprocessing
import threading
import time
import traceback
import queue
import random
import datetime
import signal

# import sqlalchemy.exc
# from sqlalchemy.sql import text

import psycopg2

import settings
# import WebMirror.database as db
import WebMirror.LogBase as LogBase
import WebMirror.OutputFilters.AmqpInterface
import runStatus

########################################################################################################################
#
#	##     ##    ###    #### ##    ##     ######  ##          ###     ######   ######
#	###   ###   ## ##    ##  ###   ##    ##    ## ##         ## ##   ##    ## ##    ##
#	#### ####  ##   ##   ##  ####  ##    ##       ##        ##   ##  ##       ##
#	## ### ## ##     ##  ##  ## ## ##    ##       ##       ##     ##  ######   ######
#	##     ## #########  ##  ##  ####    ##       ##       #########       ##       ##
#	##     ## ##     ##  ##  ##   ###    ##    ## ##       ##     ## ##    ## ##    ##
#	##     ## ##     ## #### ##    ##     ######  ######## ##     ##  ######   ######
#
########################################################################################################################



NO_JOB_TIMEOUT_MINUTES = 5
# MAX_IN_FLIGHT_JOBS = 10
# MAX_IN_FLIGHT_JOBS = 75
# MAX_IN_FLIGHT_JOBS = 250
MAX_IN_FLIGHT_JOBS = 500
# MAX_IN_FLIGHT_JOBS = 1000
# MAX_IN_FLIGHT_JOBS = 3000

def buildjob(
			module,
			call,
			dispatchKey,
			jobid,
			args           = [],
			kwargs         = {},
			additionalData = None,
			postDelay      = 0
		):

	job = {
			'call'         : call,
			'module'       : module,
			'args'         : args,
			'kwargs'       : kwargs,
			'extradat'     : additionalData,
			'jobid'        : jobid,
			'dispatch_key' : dispatchKey,
			'postDelay'    : postDelay,
		}
	return job



class JobAggregator(LogBase.LoggerMixin):

	loggerPath = "Main.JobAggregator"

	def __init__(self):
		# print("Job __init__()")
		super().__init__()

		self.last_rx = datetime.datetime.now()
		self.active_jobs = 0
		self.jobs_out = 0
		self.jobs_in = 0


		self.db_interface = psycopg2.connect(
				database = settings.DATABASE_DB_NAME,
				user     = settings.DATABASE_USER,
				password = settings.DATABASE_PASS,
				host     = settings.DATABASE_IP,
			)

		# This queue has to be a multiprocessing queue, because it's shared across multiple processes.
		self.normal_out_queue  = multiprocessing.Queue()

		self.j_fetch_proc = threading.Thread(target=self.queue_filler_proc)
		self.j_fetch_proc.start()

		self.print_mod = 0

	def get_queues(self):
		return self.normal_out_queue

	def join_proc(self):
		runStatus.job_run_state.value = 0
		self.j_fetch_proc.join(0)

	def put_outbound_job(self, jobid, joburl):
		self.active_jobs += 1
		self.log.info("Dispatching new job (active jobs: %s)", self.active_jobs)
		self.jobs_out += 1
		raw_job = buildjob(
			module         = 'WebRequest',
			call           = 'getItem',
			dispatchKey    = "fetcher",
			jobid          = jobid,
			args           = [joburl],
			kwargs         = {},
			additionalData = {'mode' : 'fetch'},
			postDelay      = 0
		)
		self.amqp_int.put_job(raw_job)
		# print("Raw job:", raw_job)
		# print("Jobid, joburl: ", (jobid, joburl))

	def fill_jobs(self):
		if 'drain' in sys.argv:
			return

		while self.active_jobs < MAX_IN_FLIGHT_JOBS and self.normal_out_queue.qsize() < MAX_IN_FLIGHT_JOBS:
			self.log.info("Need to add jobs to the job queue (%s active)!", self.active_jobs)
			self._get_task_internal()

			# We have to handle job responses here too, or the response queue can bloat horribly
			# while we're waiting for the output job queue to fill.
			self.process_responses()
			if runStatus.run_state.value != 1:
				return

		# If we haven't had a received job in 10 minutes, reset the job counter because we might
		# have leaked the jobs away somehow.
		if (self.last_rx + datetime.timedelta(minutes=NO_JOB_TIMEOUT_MINUTES)) < datetime.datetime.now():
			if self.normal_out_queue.qsize() > MAX_IN_FLIGHT_JOBS:
				self.log.warn("Long latency since last received job, but received job queue contains lots of jobs. Huh? (Jobqueue size: %s)", self.normal_out_queue.qsize())
			else:
				self.log.error("Timeout since last job seen. Resetting active job counter. (lastJob: %s)", self.last_rx + datetime.timedelta(minutes=NO_JOB_TIMEOUT_MINUTES))
				self.active_jobs = 0
				self.last_rx = datetime.datetime.now()

	def process_responses(self):
		while 1:
			tmp = self.amqp_int.get_job()
			if tmp:
				self.active_jobs -= 1
				self.jobs_in += 1
				if self.active_jobs < 0:
					self.active_jobs = 0
				self.log.info("Job response received. Jobs in-flight: %s", self.active_jobs)
				self.last_rx = datetime.datetime.now()
				self.normal_out_queue.put(tmp)
			else:
				self.print_mod += 1
				if self.print_mod > 20:
					self.log.info("No job responses available.")
					self.print_mod = 0
				break

	def queue_filler_proc(self):

		amqp_settings = {
			'RABBIT_LOGIN'    : settings.RPC_RABBIT_LOGIN,
			'RABBIT_PASWD'    : settings.RPC_RABBIT_PASWD,
			'RABBIT_SRVER'    : settings.RPC_RABBIT_SRVER,
			'RABBIT_VHOST'    : settings.RPC_RABBIT_VHOST,
			'master'          : True,
			# 'prefetch'        : 250,
			# 'prefetch'        : 50,
			'prefetch'        : 5,
			'queue_mode'      : 'direct',
			'taskq_task'      : 'task.q',
			'taskq_response'  : 'response.q',

			"poll_rate"       : 1/100,

		}


		self.amqp_int = WebMirror.OutputFilters.AmqpInterface.RabbitQueueHandler(amqp_settings)

		try:
			signal.signal(signal.SIGINT, signal.SIG_IGN)
		except ValueError:
			self.log.warning("Cannot configure job fetcher task to ignore SIGINT. May be an issue.")

		self.log.info("Job queue fetcher starting.")


		msg_loop = 0
		while runStatus.job_run_state.value == 1:
			self.fill_jobs()
			self.process_responses()

			msg_loop += 1
			time.sleep(1)
			if msg_loop > 20:
				self.log.info("Job queue filler process. Current job queue size: %s (out: %s, in: %s). Runstate: %s", self.active_jobs, self.jobs_out, self.jobs_in, runStatus.job_run_state.value==1)
				msg_loop = 0

		self.log.info("Job queue fetcher saw exit flag. Halting.")
		self.amqp_int.close()

		# Consume the remaining items in the output queue so it shuts down cleanly.
		try:
			while 1:
				self.normal_out_queue.get_nowait()
		except queue.Empty:
			pass

		self.log.info("Job queue filler process. Current job queue size: %s. Runstate: %s", self.active_jobs, runStatus.job_run_state.value==1)

		self.log.info("Job queue fetcher halted.")


	def _get_task_internal(self):

		cursor = self.db_interface.cursor()
		# Hand-tuned query, I couldn't figure out how to
		# get sqlalchemy to emit /exactly/ what I wanted.
		# TINY changes will break the query optimizer, and
		# the 10 ms query will suddenly take 10 seconds!
		raw_query = '''
				UPDATE
				    web_pages
				SET
				    state = 'fetching'
				WHERE
				    web_pages.id IN (
				        SELECT
				            web_pages.id
				        FROM
				            web_pages
				        WHERE
				            web_pages.state = 'new'
				        AND
				            normal_fetch_mode = true
				        AND
				            web_pages.priority = (
				               SELECT
				                    min(priority)
				                FROM
				                    web_pages
				                WHERE
				                    state = 'new'::dlstate_enum
				                AND
				                    distance < 1000000
				                AND
				                    normal_fetch_mode = true
				                AND
				                    web_pages.ignoreuntiltime < now() + '5 minutes'::interval
				            )
				        AND
				            web_pages.distance < 1000000
				        AND
				            web_pages.ignoreuntiltime < now() + '5 minutes'::interval
				        LIMIT {in_flight}
				    )
				AND
				    web_pages.state = 'new'
				RETURNING
				    web_pages.id, web_pages.netloc, web_pages.url;
			'''.format(in_flight=50)


		start = time.time()

		while runStatus.run_state.value == 1:
			try:
				cursor.execute(raw_query)
				rids = cursor.fetchall()
				self.db_interface.commit()
				break
			except psycopg2.Error:
				delay = random.random() / 3
				# traceback.print_exc()
				self.log.warn("Error getting job (psycopg2.Error)! Delaying %s.", delay)
				time.sleep(delay)
				self.db_interface.rollback()

		if runStatus.run_state.value != 1:
			return

		if not rids:
			return

		rids = list(rids)
		# If we broke because a user-interrupt, we may not have a
		# valid rids at this point.
		if runStatus.run_state.value != 1:
			return False

		xqtim = time.time() - start

		if len(rids) == 0:
			self.log.warning("No jobs available! Sleeping for 5 seconds waiting for new jobs to become available!")
			for dummy_x in range(5):
				if runStatus.run_state.value == 1:
					time.sleep(1)
			return

		if xqtim > 0.5:
			self.log.error("Query execution time: %s ms. Fetched job IDs = %s", xqtim * 1000, len(rids))
		elif xqtim > 0.1:
			self.log.warn("Query execution time: %s ms. Fetched job IDs = %s", xqtim * 1000, len(rids))
		else:
			self.log.info("Query execution time: %s ms. Fetched job IDs = %s", xqtim * 1000, len(rids))
		deleted = 0
		for rid, netloc, joburl in rids:
			self.put_outbound_job(rid, joburl)

		cursor.close()


def test2():
	import logSetup
	import pprint
	logSetup.initLogging()

	agg = JobAggregator()
	outq = agg.get_queues()
	for x in range(20):
		print("Sleeping, ", x)
		time.sleep(1)
		try:
			j = outq.get_nowait()
			print("Received job! %s", len(j))
			with open("jobs.txt", "a") as fp:
				fp.write("\n\n\n")
				fp.write(pprint.pformat(j))
			print(j)
		except queue.Empty:
			pass
	print("Joining on the aggregator")
	agg.join_proc()
	print("Joined.")

if __name__ == "__main__":
	test2()


