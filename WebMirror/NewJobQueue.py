import sys
import multiprocessing
import gc
import time
import traceback
import queue
import random
import datetime
import signal

# import sqlalchemy.exc
# from sqlalchemy.sql import text

import psycopg2
import bsonrpc.exceptions
import sys
import os

import settings
import common.global_constants
# import common.database as db
import common.LogBase as LogBase
import WebMirror.rules
# import WebMirror.OutputFilters.AmqpInterface
import common.get_rpyc
import zerorpc
import runStatus
import WebMirror.SpecialCase

import mem_top
from pympler.tracker import SummaryTracker

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



NO_JOB_TIMEOUT_MINUTES = 15

JOB_QUERY_CHUNK_SIZE = 250

largv = [tmp.lower() for tmp in sys.argv]
if "twoprocess" in largv or "oneprocess" in largv:
	MAX_IN_FLIGHT_JOBS = 10
else:
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
			postDelay      = 0,
			extra_keys     = {},
			unique_id      = None,
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
	if unique_id is not None:
		job['unique_id'] = unique_id
	return job



class JobAggregatorInternal(LogBase.LoggerMixin):

	loggerPath = "Main.JobAggregator"

	def __init__(self, job_queue, run_flag):
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

		self.normal_out_queue = job_queue
		self.run_flag = run_flag



	def run(self):


		self.print_mod = 0

		self.ruleset = WebMirror.rules.load_rules()
		self.specialcase = WebMirror.rules.load_special_case_sites()
		self.tracker = SummaryTracker()
		self.tracker.diff()
		self.queue_filler_proc()

	def get_queues(self):
		return self.normal_out_queue

	def join_proc(self):
		self.log.info("Setting exit flag on processor.")
		runStatus.job_run_state.value = 0
		self.log.info("Joining on worker thread.")
		self.j_fetch_proc.join(0)

	def put_outbound_job(self, jobid, joburl):
		self.active_jobs += 1
		self.log.info("Dispatching new job (active jobs: %s of %s)", self.active_jobs, MAX_IN_FLIGHT_JOBS)
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

		# Recycle the rpc interface if it ded
		errors = 0
		while 1:
			try:
				self.rpc_interface.put_job(raw_job)
				return
			except TypeError:
				self.check_open_rpc_interface()
			except KeyError:
				self.check_open_rpc_interface()
			except bsonrpc.exceptions.BsonRpcError as e:
				errors += 1
				self.check_open_rpc_interface()
				if errors > 3:
					raise e
				else:
					self.log.warning("Exception in RPC request:")
					for line in traceback.format_exc().split("\n"):
						self.log.warning(line)



	def generalLinkClean(self, link, badwords):
		if link.startswith("data:"):
			return None
		linkl = link.lower()
		if any([badword in linkl for badword in badwords]):

			print("Filtered:", link, [badword for badword in badwords if badword in linkl ])
			return None
		return link

	def getBadWords(self, netloc):
		badwords = [tmp for tmp in common.global_constants.GLOBAL_BAD_URLS]
		for item in [rules for rules in self.ruleset if rules['netlocs'] and netloc in rules['netlocs']]:
			badwords += item['badwords']

		# A "None" can occationally crop up. Filter it.
		badwords = [badword for badword in badwords if badword]
		badwords = [badword.lower() for badword in badwords]
		badwords = list(set(badwords))
		return badwords

	def outbound_job_wanted(self, netloc, joburl):
		badwords = self.getBadWords(netloc)

		ret = self.generalLinkClean(joburl, badwords)
		if ret:
			return True

		self.log.warn("Unwanted URL: '%s' - %s", joburl, ret)

		return False

	def delete_job(self, rid, joburl):
		self.log.warning("Deleting job for url: '%s'", joburl)
		cursor = self.db_interface.cursor()
		cursor.execute("""DELETE FROM web_pages WHERE web_pages.id = %s AND web_pages.url = %s;""", (rid, joburl))
		self.db_interface.commit()

	def fill_jobs(self):
		if 'drain' in sys.argv:
			return

		while self.active_jobs < MAX_IN_FLIGHT_JOBS and self.normal_out_queue.qsize() < MAX_IN_FLIGHT_JOBS:
			old = self.active_jobs
			num_new  = self._get_task_internal()
			num_new += self._get_deferred_internal()
			self.log.info("Need to add jobs to the job queue (%s active, %s added, queue: %s)!", self.active_jobs, self.active_jobs-old, self.normal_out_queue.qsize())



			# We have to handle job responses here too, or the response queue can bloat horribly
			# while we're waiting for the output job queue to fill.
			self.process_responses()
			if runStatus.run_state.value != 1:
				return

			# If there weren't any new items, stop looping because we're not going anywhere.
			if num_new == 0:
				break

		# If we haven't had a received job in 10 minutes, reset the job counter because we might
		# have leaked the jobs away somehow.
		if (self.last_rx + datetime.timedelta(minutes=NO_JOB_TIMEOUT_MINUTES)) < datetime.datetime.now():
			if self.normal_out_queue.qsize() > MAX_IN_FLIGHT_JOBS:
				self.log.warn("Long latency since last received job, but received job queue contains lots of jobs. Huh? (Jobqueue size: %s)", self.normal_out_queue.qsize())
			else:
				self.log.error("Timeout since last job seen. Resetting active job counter. (lastJob: %s)", self.last_rx + datetime.timedelta(minutes=NO_JOB_TIMEOUT_MINUTES))
				self.active_jobs = 0
				self.last_rx = datetime.datetime.now()

	def __blocking_put(self, item):
		while runStatus.job_run_state.value == 1:
			try:
				self.normal_out_queue.put_nowait(item)
				return
			except queue.Full:
				self.log.warning("Response queue full ({} items). Sleeping", self.normal_out_queue.qsize())
				time.sleep(1)

	def process_responses(self):
		while 1:

			# Something in the RPC stuff is resulting in a typeerror I don't quite
			# understand the source of. anyways, if that happens, just reset the RPC interface.
			try:
				tmp = self.rpc_interface.get_job()
			except queue.Empty:
				return

			except TypeError:
				self.check_open_rpc_interface()
				return
			except KeyError:
				self.check_open_rpc_interface()
				return

			except bsonrpc.exceptions.ResponseTimeout:
				self.check_open_rpc_interface()
				return


			if tmp:
				self.active_jobs -= 1
				self.jobs_in += 1
				if self.active_jobs < 0:
					self.active_jobs = 0
				self.log.info("Job response received. Jobs in-flight: %s (qsize: %s)", self.active_jobs, self.normal_out_queue.qsize())
				self.last_rx = datetime.datetime.now()

				self.__blocking_put(tmp)
			else:
				self.print_mod += 1
				if self.print_mod > 20:
					self.log.info("No job responses available.")
					self.print_mod = 0
				time.sleep(1)
				break

	def check_open_rpc_interface(self):
		if not hasattr(self, "rpc_interface"):
			self.rpc_interface = common.get_rpyc.RemoteJobInterface("ProcessedMirror")
		try:
			if self.rpc_interface.check_ok():
				return


		except Exception:
			self.log.error("Failure when probing RPC interface")
			for line in traceback.format_exc().split("\n"):
				self.log.error(line)
			try:
				self.rpc_interface.close()
				self.log.info("Closed interface due to connection exception.")
			except Exception:
				self.log.error("Failure when closing errored RPC interface")
				for line in traceback.format_exc().split("\n"):
					self.log.error(line)
			self.rpc_interface = common.get_rpyc.RemoteJobInterface("ProcessedMirror")

	def __queue_fillter_internal(self):
		# try:
		# 	signal.signal(signal.SIGINT, signal.SIG_IGN)
		# except ValueError:
		# 	self.log.warning("Cannot configure job fetcher task to ignore SIGINT. May be an issue.")
		# 	for line in traceback.format_exc().split("\n"):
		# 		self.log.warning(line)

		self.check_open_rpc_interface()

		self.log.info("Job queue fetcher starting.")

		for x in range(2500):
			if not runStatus.job_run_state.value == 1:
				break
			self.fill_jobs()
			self.process_responses()

			time.sleep(2.5)
			self.log.info("Job queue filler process. Current job queue size: %s (out: %s, in: %s). Runstate: %s", self.active_jobs, self.jobs_out, self.jobs_in, runStatus.job_run_state.value==1)

			self.log.info("Object diff:")
			with open("growth.txt", "a") as fp:
				fp.write("\n")
				fp.write("Growth at {}\n".format(time.time()))
				fp.write("Queue size: {}\n".format(self.normal_out_queue.qsize()))

				# diff = self.tracker.format_diff()
				# if not diff:
				# 	diff.append("	No changes")
				# for line in diff:
				# 	fp.write("{}\n".format(line))
				# 	self.log.info(line)
				# self.log.info("")
			gc.collect()

		self.log.info("Job queue fetcher saw exit flag. Halting.")
		self.rpc_interface.close()


	def queue_filler_proc(self):


		while self.run_flag.value == 1:
			try:

				self.__queue_fillter_internal()
			except ConnectionRefusedError:
				self.log.warning("RPC Remote appears to not be listening!")
				time.sleep(1)
			except Exception as e:
				with open("error - {}.txt".format(time.time()), "w") as fp:
					fp.write("Wat? Exception!\n\n")
					fp.write(traceback.format_exc())
				for line in traceback.format_exc().split("\n"):
					self.log.error(line)

		# Consume the remaining items in the output queue so it shuts down cleanly.
		try:
			while 1:
				self.normal_out_queue.get_nowait()
		except queue.Empty:
			pass

		self.log.info("Job queue filler process. Current job queue size: %s. Runstate: %s", self.active_jobs, runStatus.job_run_state.value==1)

		self.log.info("Job queue fetcher halted.")

	def _get_deferred_internal(self):
		rid, joburl, netloc = WebMirror.SpecialCase.getSpecialCase(self.specialcase)
		newcnt = 0
		while rid:
			self.put_outbound_job(rid, joburl)
			newcnt += 1
			rid, joburl, netloc = WebMirror.SpecialCase.getSpecialCase(self.specialcase)

		return newcnt

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
			'''.format(in_flight=min((MAX_IN_FLIGHT_JOBS, JOB_QUERY_CHUNK_SIZE)))


		start = time.time()

		while runStatus.run_state.value == 1:
			try:
				cursor.execute(raw_query)
				rids = cursor.fetchall()
				cursor.execute("COMMIT;")
				break
			except psycopg2.Error:
				delay = random.random() / 3
				# traceback.print_exc()
				self.log.warn("Error getting job (psycopg2.Error)! Delaying %s.", delay)
				time.sleep(delay)
				cursor.execute("ROLLBACK;")

		if runStatus.run_state.value != 1:
			return 0

		if not rids:
			return 0

		rids = list(rids)
		# If we broke because a user-interrupt, we may not have a
		# valid rids at this point.
		if runStatus.run_state.value != 1:
			return 0

		xqtim = time.time() - start

		if len(rids) == 0:
			self.log.warning("No jobs available! Sleeping for 5 seconds waiting for new jobs to become available!")
			for dummy_x in range(5):
				if runStatus.run_state.value == 1:
					time.sleep(1)
			return 0

		if xqtim > 0.5:
			self.log.error("Query execution time: %s ms. Fetched job IDs = %s", xqtim * 1000, len(rids))
		elif xqtim > 0.1:
			self.log.warn("Query execution time: %s ms. Fetched job IDs = %s", xqtim * 1000, len(rids))
		else:
			self.log.info("Query execution time: %s ms. Fetched job IDs = %s", xqtim * 1000, len(rids))
		deleted = 0
		for rid, netloc, joburl in rids:
			if not self.outbound_job_wanted(netloc, joburl):
				self.delete_job(rid, joburl)
			elif WebMirror.SpecialCase.haveSpecialCase(self.specialcase, joburl, netloc):
				pass
				# WebMirror.SpecialCase.pushSpecialCase(self.specialcase, rid, joburl, netloc)
			else:
				self.put_outbound_job(rid, joburl)

		cursor.close()

		return len(rids)

def run_shim(job_queue, run_flag):
	instance = JobAggregatorInternal(job_queue, run_flag)
	instance.run()


class AggregatorWrapper():
	def __init__(self, start_worker=True):
		# This queue has to be a multiprocessing queue, because it's shared across multiple processes.
		self.normal_out_queue  = multiprocessing.Queue(maxsize=MAX_IN_FLIGHT_JOBS)
		self.run_flag = multiprocessing.Value("b", 1)
		if start_worker:
			self.main_job_agg = multiprocessing.Process(target=run_shim, args=(self.normal_out_queue, self.run_flag))
			self.main_job_agg.start()
		else:
			self.main_job_agg = None


	def get_queues(self):
		return self.normal_out_queue

	def join_proc(self):
		self.run_flag.value = 0

		if self.main_job_agg:
			self.main_job_agg.join()



def test2():
	import logSetup
	import pprint
	logSetup.initLogging()

	specialcase = WebMirror.rules.load_special_case_sites()
	WebMirror.SpecialCase.pushSpecialCase(specialcase, 0, "http://www.novelupdates.com/1", "www.novelupdates.com")
	WebMirror.SpecialCase.pushSpecialCase(specialcase, 0, "http://www.novelupdates.com/2", "www.novelupdates.com")



	for x in range(30):
		print("Sleeping, ", x)
		time.sleep(1)
		ret = WebMirror.SpecialCase.getSpecialCase(specialcase)
		print("Return: ", ret)
		if x == 15:
			WebMirror.SpecialCase.pushSpecialCase(specialcase, 0, "http://www.novelupdates.com/3", "www.novelupdates.com")
			WebMirror.SpecialCase.pushSpecialCase(specialcase, 0, "http://www.novelupdates.com/4", "www.novelupdates.com")

	print("Done!")

if __name__ == "__main__":
	test2()


