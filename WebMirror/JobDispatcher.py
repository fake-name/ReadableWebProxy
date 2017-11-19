import sys
import multiprocessing
import gc
import time
import traceback
import queue
import random
import datetime
import threading
import signal
import socket

# import sqlalchemy.exc
# from sqlalchemy.sql import text

import cachetools
import psycopg2
import bsonrpc.exceptions
import sys
import os

import settings
import common.NetlocThrottler
import common.global_constants
import common.util.urlFuncs
import common.LogBase as LogBase
import WebMirror.rules
import common.get_rpyc
import runStatus
import WebMirror.SpecialCase
import WebMirror.JobUtils

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
	# MAX_IN_FLIGHT_JOBS = 100
	# MAX_IN_FLIGHT_JOBS = 250
	# MAX_IN_FLIGHT_JOBS = 500
	# MAX_IN_FLIGHT_JOBS = 1000
	MAX_IN_FLIGHT_JOBS = 2500
	# MAX_IN_FLIGHT_JOBS = 3000

class RpcMixin():
	def check_open_rpc_interface(self):
		for _ in range(5):
			try:

				if not hasattr(self, "rpc_interface"):
					self.rpc_interface = common.get_rpyc.RemoteJobInterface("ProcessedMirror")

				if self.rpc_interface.check_ok():
					return
				else:
					self.log.error("RPC Interface not OK?")
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
				self.rpc_interface.check_ok()

		raise RuntimeError("RPC interface appears to not be active. Nothing to do?")

class RpcJobConsumerInternal(LogBase.LoggerMixin, RpcMixin):
	loggerPath = "Main.JobConsumer"

	def __init__(self, job_queue, run_flag, system_state):
		# print("Job __init__()")
		super().__init__()


		self.normal_out_queue = job_queue
		self.run_flag         = run_flag
		self.system_state     = system_state


		self.last_rx = datetime.datetime.now()

		self.print_mod = 0


	def __blocking_put_response(self, item):
		while self.run_flag.value == 1:
			try:
				self.normal_out_queue.put_nowait(item)
				return
			except queue.Full:
				self.log.warning("Response queue full (%s items). Sleeping", self.normal_out_queue.qsize())
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

				nl = None
				if 'extradat' in tmp and 'netloc' in tmp['extradat']:
					nl = tmp['extradat']['netloc']

				with self.system_state['lock']:
					self.system_state['active_jobs']     -= 1
					self.system_state['jobs_in']         += 1
					self.system_state['active_jobs']      = max(self.system_state['active_jobs'], 0)
					self.system_state['qsize']            = self.normal_out_queue.qsize()

					if nl:
						if 'success' in tmp and tmp['success']:
							self.system_state['ratelimiter'].netloc_ok(nl)
						else:
							self.system_state['ratelimiter'].netloc_error(nl)
					else:
						self.log.warning("Missing netloc in response extradat!")

				self.log.info("Job response received. Jobs in-flight: %s (qsize: %s)", self.system_state['active_jobs'], self.normal_out_queue.qsize())
				self.last_rx = datetime.datetime.now()

				self.__blocking_put_response(tmp)
			else:

				with self.system_state['lock']:
					self.system_state['qsize']            = self.normal_out_queue.qsize()

				self.print_mod += 1
				if self.print_mod > 20:
					self.log.info("No job responses available.")
					self.print_mod = 0
				time.sleep(1)
				break

		# If we haven't had a received job in 10 minutes, reset the job counter because we might
		# have leaked the jobs away somehow.
		if (self.last_rx + datetime.timedelta(minutes=NO_JOB_TIMEOUT_MINUTES)) < datetime.datetime.now():
			if self.normal_out_queue.qsize() > MAX_IN_FLIGHT_JOBS:
				self.log.warn("Long latency since last received job, but received job queue contains lots of jobs. Huh? (Jobqueue size: %s)", self.normal_out_queue.qsize())
			else:
				self.log.error("Timeout since last job seen. Resetting active job counter. (lastJob: %s)", self.last_rx + datetime.timedelta(minutes=NO_JOB_TIMEOUT_MINUTES))

				with self.system_state['lock']:
					self.system_state['active_jobs']     = 0

				self.last_rx = datetime.datetime.now()

	def __queue_consumer_internal(self):

		self.check_open_rpc_interface()

		self.log.info("Job queue consumer starting.")

		for _ in range(100):
			if not self.run_flag.value == 1:
				break
			self.process_responses()

			time.sleep(0.5)
			self.log.info("Job queue consumer process. Current job queue size: %s (out: %s, in: %s). Runstate: %s",
				self.system_state['active_jobs'], self.system_state['jobs_out'], self.system_state['jobs_in'], self.run_flag.value)

		self.log.info("Job queue consumer saw exit flag. Halting.")
		self.rpc_interface.close()
		gc.collect()


	def consume(self):


		while self.run_flag.value == 1:
			print("Queue consumer looping!")
			try:

				self.__queue_consumer_internal()
			except ConnectionRefusedError:
				self.log.warning("(ConnectionRefusedError) RPC Remote appears to not be listening!")
				time.sleep(1)
			except socket.timeout:
				self.log.warning("(socket.timeout) RPC Remote appears to not be listening!")
				time.sleep(1)
			except Exception as e:
				with open("error %s - %s.txt" % ('job_consumer', time.time()), "w") as fp:
					fp.write("Manager crashed?\n")
					fp.write(traceback.format_exc())
				for line in traceback.format_exc().split("\n"):
					self.log.error(line)

		# Consume the remaining items in the output queue so it shuts down cleanly.
		try:
			while 1:
				self.normal_out_queue.get_nowait()
		except queue.Empty:
			pass

		self.log.info("Job queue fetcher halted.")

	def run(self):
		try:
			self.consume()

		except Exception:
			with open("error %s - %s.txt" % ('job_consumer', time.time()), "w") as fp:
				fp.write("Manager crashed?\n")
				fp.write(traceback.format_exc())
			raise


class RpcJobDispatcherInternal(LogBase.LoggerMixin, RpcMixin):

	loggerPath = "Main.JobDispatcher"

	def __init__(self, mode, run_flag, system_state):
		# print("Job __init__()")
		self.loggerPath = "Main.JobDispatcher(%s)" % mode

		super().__init__()

		self.last_rx = datetime.datetime.now()


		self.db_interface = psycopg2.connect(
				database = settings.DATABASE_DB_NAME,
				user     = settings.DATABASE_USER,
				password = settings.DATABASE_PASS,
				host     = settings.DATABASE_IP,
			)

		self.system_state = system_state
		self.jq_mode      = mode
		self.run_flag     = run_flag

		self.ruleset        = WebMirror.rules.load_rules()
		self.specialcase    = WebMirror.rules.load_special_case_sites()
		self.triggerUrls    = set(WebMirror.rules.load_triggered_url_list())
		self.print_mod = 0


	def join_proc(self):
		self.log.info("Setting exit flag on processor.")
		runStatus.job_run_state.value = 0
		self.log.info("Joining on worker thread.")


	def put_job(self, raw_job):

		# Recycle the rpc interface if it ded
		errors = 0
		while 1:
			try:
				self.rpc_interface.put_job(raw_job)
				with self.system_state['lock']:
						self.system_state['active_jobs'] += 1
						self.system_state['jobs_out'] += 1

				self.log.info("Dispatched new job (active jobs: %s of %s)", self.system_state['active_jobs'], MAX_IN_FLIGHT_JOBS)
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


	def put_fetch_job(self, jobid, joburl, netloc=None):
		# module='WebRequest', call='getItem'
		raw_job = WebMirror.JobUtils.buildjob(
			module         = 'WebRequest',
			call           = 'getItem',
			dispatchKey    = "fetcher",
			jobid          = jobid,
			args           = [joburl],
			kwargs         = {},
			additionalData = {'mode' : 'fetch', 'netloc' : netloc},
			postDelay      = 0
		)

		self.put_job(raw_job)

	def generalLinkClean(self, link, badwords, badcompounds):
		if link.startswith("data:"):
			return None
		linkl = link.lower()
		if any([badword in linkl for badword in badwords]):
			print("Filtered:", link, [badword for badword in badwords if badword in linkl ])
			return None

		if any([all([badword in linkl for badword in badcompound]) for badcompound in badcompounds]):
			print("Compound Filtered:", link, [badword for badword in badwords if badword in linkl ])
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

		badcompounds = []

		for item in [rules for rules in self.ruleset if rules['netlocs'] and netloc in rules['netlocs']]:
			if item['compound_badwords']:
				badcompounds += item['compound_badwords']

		return badwords, badcompounds


	def outbound_job_wanted(self, netloc, joburl):

		disallowDupe = False
		for ruleset in self.ruleset:
			if ruleset['netlocs'] and netloc in ruleset['netlocs']:
				disallowDupe = ruleset['disallow_duplicate_path_segments'] or disallowDupe

		if disallowDupe:
			bad = common.util.urlFuncs.hasDuplicatePathSegments(joburl)
			if bad:
				self.log.warn("Unwanted URL (pathchunks): '%s' - %s", joburl, bad)
				return False


		badwords, badcompounds = self.getBadWords(netloc)
		ret = self.generalLinkClean(joburl, badwords, badcompounds)
		if ret:
			return True

		if joburl in self.triggerUrls:
			return True

		self.log.warn("Unwanted URL: '%s' - %s", joburl, ret)

		return False

	def delete_job(self, rid, joburl):
		self.log.warning("Deleting job for url: '%s'", joburl)
		cursor = self.db_interface.cursor()
		cursor.execute("""DELETE FROM web_pages         WHERE web_pages.id = %s         AND web_pages.url = %s;""", (rid, joburl))
		cursor.execute("""DELETE FROM web_pages_version WHERE web_pages_version.id = %s AND web_pages_version.url = %s;""", (rid, joburl))
		self.db_interface.commit()

	def fill_jobs(self):
		if 'drain' in sys.argv:
			return
		total_new = 0
		while self.system_state['active_jobs'] < MAX_IN_FLIGHT_JOBS and self.system_state['qsize'] < 100:
			old = self.system_state['active_jobs']
			num_new = self._get_task_internal()
			num_new += self._get_deferred_internal()
			self.log.info("Need to add jobs to the job queue (%s active, %s added)!", self.system_state['active_jobs'], self.system_state['active_jobs']-old)

			if runStatus.run_state.value != 1:
				return

			total_new += num_new

			# If there weren't any new items, stop looping because we're not going anywhere.
			if num_new == 0:
				break

		return total_new


	def __queue_fillter_internal(self):
		# try:
		# 	signal.signal(signal.SIGINT, signal.SIG_IGN)
		# except ValueError:
		# 	self.log.warning("Cannot configure job fetcher task to ignore SIGINT. May be an issue.")
		# 	for line in traceback.format_exc().split("\n"):
		# 		self.log.warning(line)

		self.check_open_rpc_interface()

		self.log.info("Job queue fetcher starting.")

		for _ in range(1000):
			if not runStatus.job_run_state.value == 1:
				break
			newj = self.fill_jobs()

			time.sleep(0.5)
			self.log.info("Job queue filler process. Added %s, active jobs: %s (out: %s, in: %s, pq: %s, deferred: %s). Runstate: %s",
				newj, self.system_state['active_jobs'], self.system_state['jobs_out'], self.system_state['jobs_in'], self.system_state['qsize'],
				self.system_state['ratelimiter'].get_in_queues(), self.run_flag.value)

		self.log.info("Job queue fetcher saw exit flag. Halting.")
		self.rpc_interface.close()
		gc.collect()


	def queue_filler_proc(self):


		while self.run_flag.value == 1:
			print("Queue filler looping!")
			try:

				self.__queue_fillter_internal()
			except ConnectionRefusedError:
				self.log.warning("(ConnectionRefusedError) RPC Remote appears to not be listening!")
				time.sleep(1)
			except socket.timeout:
				self.log.warning("(socket.timeout) RPC Remote appears to not be listening!")
				time.sleep(1)
			except Exception as e:

				with open("error %s - %s.txt" % (self.jq_mode, time.time()), "w") as fp:
					fp.write("Manager crashed?\n")
					fp.write(traceback.format_exc())
				# with open("error - {}.txt".format(time.time()), "w") as fp:
				# 	fp.write("Wat? Exception!\n\n")
				# 	fp.write(traceback.format_exc())
				for line in traceback.format_exc().split("\n"):
					self.log.error(line)

		self.log.info("Job queue filler process halting. Current job queue size: %s. Runstate: %s", self.system_state['active_jobs'], self.run_flag.value)
		self.log.info("Job queue fetcher halted.")

	def _get_deferred_internal(self):
		rid, joburl, netloc = WebMirror.SpecialCase.getSpecialCase(self.specialcase)
		newcnt = 0
		while rid:
			self.put_fetch_job(rid, joburl, netloc)
			newcnt += 1
			rid, joburl, dummy_netloc = WebMirror.SpecialCase.getSpecialCase(self.specialcase)

		with self.system_state['lock']:
			new_j_l =self.system_state['ratelimiter'].get_available_jobs()

		for rid, joburl, netloc in new_j_l:
			self.put_fetch_job(rid, joburl, netloc)
			newcnt += 1

		return newcnt

	def _get_task_internal(self):

		cursor = self.db_interface.cursor()
		# Hand-tuned query, I couldn't figure out how to
		# get sqlalchemy to emit /exactly/ what I wanted.
		# TINY changes will break the query optimizer, and
		# the 10 ms query will suddenly take 10 seconds!
		raw_query_never_fetched = '''
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

		raw_query_any = '''
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
				            web_pages.distance < 1000000
				        LIMIT {in_flight}
				    )
				AND
				    web_pages.state = 'new'
				RETURNING
				    web_pages.id, web_pages.netloc, web_pages.url;
			'''.format(in_flight=min((MAX_IN_FLIGHT_JOBS, JOB_QUERY_CHUNK_SIZE)))

		raw_query_ordered = '''
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
				if self.jq_mode == 'priority':
					cursor.execute(raw_query_ordered)
					rids = cursor.fetchall()
				elif self.jq_mode == 'new_fetch':
					cursor.execute(raw_query_never_fetched)
					rids = cursor.fetchall()
				elif self.jq_mode == 'random':
					cursor.execute(raw_query_any)
					rids = cursor.fetchall()
				else:
					self.log.error("Unknown job queue dispatcher mode: %s", self.jq_mode)
					rids = []


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

		defer = []
		for rid, netloc, joburl in rids:
			if "booksie" in netloc:
				continue
			if not self.outbound_job_wanted(netloc, joburl):
				self.delete_job(rid, joburl)
			elif WebMirror.SpecialCase.haveSpecialCase(self.specialcase, joburl, netloc):
				WebMirror.SpecialCase.pushSpecialCase(self.specialcase, rid, joburl, netloc, self)
			else:
				defer.append((rid, joburl, netloc))
				# self.put_fetch_job(rid, joburl, netloc)

		with self.system_state['lock']:
			for rid_d, joburl_d, netloc_d in defer:
				self.system_state['ratelimiter'].put_job(rid_d, joburl_d, netloc_d)

		cursor.close()

		if len(rids) == 0:
			self.log.warning("No jobs to dispatch in query response!?")


		return len(rids)


	def run(self):
		try:
			self.queue_filler_proc()
		except Exception:
			with open("error %s - %s.txt" % (self.jq_mode, time.time()), "w") as fp:
				fp.write("Manager crashed?\n")
				fp.write(traceback.format_exc())
			raise


class MultiRpcRunner(LogBase.LoggerMixin):
	loggerPath = "Main.MultiRpcRunner"

	def __init__(self, job_queue, run_flag):
		super().__init__()

		self.log.info("MultiRpcRunner creating RPC feeder/consumer threads")
		self.job_queue = job_queue
		self.run_flag  = run_flag

	def run(self):

		system_state = {
			'active_jobs' : 0,
			'jobs_out'    : 0,
			'jobs_in'     : 0,
			'qsize'       : 0,
			'ratelimiter' : common.NetlocThrottler.NetlockThrottler(),

			'lock'        : threading.Lock()
		}

		new_fetch_proc      = RpcJobDispatcherInternal('priority',   self.run_flag, system_state)
		priority_fetch_proc = RpcJobDispatcherInternal('new_fetch',  self.run_flag, system_state)
		random_fetch_proc   = RpcJobDispatcherInternal('random',     self.run_flag, system_state)
		job_consumer_proc   = RpcJobConsumerInternal(self.job_queue, self.run_flag, system_state)


		threads = [
			threading.Thread(target=new_fetch_proc.run),
			threading.Thread(target=priority_fetch_proc.run),
			threading.Thread(target=random_fetch_proc.run),
			threading.Thread(target=job_consumer_proc.run),
		]

		self.log.info("MultiRpcRunner starting RPC feeder/consumer threads")
		for thread in threads:
			thread.start()

		self.log.info("MultiRpcRunner threads started")

		last_reduce = 0

		while self.run_flag.value == 1:
			for x in range(10):
				time.sleep(1)
				if not self.run_flag.value:
					break
			self.log.info("Active jobs: %s", [tmp.is_alive() for tmp in threads])



			# Every 90 seconds, we deincrement the active jobs counts.
			last_reduce += 1

			if last_reduce > 10:
				last_reduce = 0
				with system_state['lock']:
					system_state['ratelimiter'].job_reduce()



		self.log.info("MultiRpcRunner exit flag seen. Joining on threads")
		for thread in threads:
			thread.join()
		self.log.info("MultiRpcRunner joined all threads. Exiting")


	@classmethod
	def run_shim(cls, job_queue, run_flag):
		try:
			instance = cls(job_queue, run_flag)
			instance.run()
		except Exception:
			print("Error!")
			print("Error!")
			print("Error!")
			print("Error!")
			traceback.print_exc()
			with open("error %s - %s.txt" % ("multijobmanager", time.time()), "w") as fp:
				fp.write("Manager crashed?\n")
				fp.write(traceback.format_exc())
			raise



class RpcJobManagerWrapper(LogBase.LoggerMixin):
	loggerPath = "Main.RpcInterfaceManager"


	def __init__(self, start_worker=True):
		super().__init__()

		self.log.info("Launching job-dispatching RPC system")

		# This queue has to be a multiprocessing queue, because it's shared across multiple processes.
		self.normal_out_queue  = multiprocessing.Queue(maxsize=MAX_IN_FLIGHT_JOBS * 2)
		self.run_flag = multiprocessing.Value("b", 1)
		if start_worker:
			self.main_job_agg = multiprocessing.Process(target=MultiRpcRunner.run_shim, args=(self.normal_out_queue, self.run_flag))
			self.main_job_agg.start()
		else:
			self.main_job_agg = None


	def get_queues(self):
		return self.normal_out_queue

	def join_proc(self):
		self.log.info("Requesting job-dispatching RPC system to halt.")
		self.run_flag.value = 0

		if self.main_job_agg:
			self.main_job_agg.join()


