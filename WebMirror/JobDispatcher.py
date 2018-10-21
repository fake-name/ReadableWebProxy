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
import contextlib
import socket


import common.stuck

# import sqlalchemy.exc
# from sqlalchemy.sql import text

import cachetools


if '__pypy__' in sys.builtin_module_names:
	import psycopg2cffi as psycopg2
else:
	import psycopg2

import sys
import os

import settings
import WebMirror.rules
import common.get_rpyc
import WebMirror.SpecialCase
import WebMirror.JobUtils

import common.NetlocThrottler
import common.global_constants
import common.util.urlFuncs

import common.LogBase as LogBase
import common.StatsdMixin as StatsdMixin

# import mem_top
# from pympler.tracker import SummaryTracker

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

@contextlib.contextmanager
def acquire_timeout(lock, timeout):
	result = lock.acquire(timeout=timeout)
	yield result
	if result:
		lock.release()

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
	# MAX_IN_FLIGHT_JOBS = 5000
	# MAX_IN_FLIGHT_JOBS = 8000

LOCAL_ENQUEUED_JOB_RESPONSES = 500

class RpcMixin():

	def __init__(self, *args, **kwargs):

		if not hasattr(self, "rpc_queue_name"):
			self.rpc_queue_name = 'ProcessedMirror'

		super().__init__(*args, **kwargs)


	def check_open_rpc_interface(self):
		for _ in range(5):
			try:

				if not hasattr(self, "rpc_interface"):
					self.log.info("Connecting using RPC queue name: '%s'", self.rpc_queue_name)
					self.rpc_interface = common.get_rpyc.RemoteJobInterface(self.rpc_queue_name)

				if self.rpc_interface.check_ok():
					return
				else:
					self.log.error("RPC Interface not OK?")
			except Exception:

				self.log.error("Failure when probing RPC interface")
				for line in traceback.format_exc().split("\n"):
					self.log.error(line)

				try:
					if hasattr(self, "rpc_interface"):
						self.rpc_interface.close()
						self.log.info("Closed interface due to connection exception.")
				except Exception:
					self.log.error("Failure when closing errored RPC interface")
					for line in traceback.format_exc().split("\n"):
						self.log.error(line)

				self.rpc_interface = common.get_rpyc.RemoteJobInterface(self.rpc_queue_name)
				self.rpc_interface.check_ok()

		raise RuntimeError("RPC interface appears to not be active. Nothing to do?")

class RpcJobConsumerInternal(LogBase.LoggerMixin, RpcMixin):
	loggerPath = "Main.JobConsumer"

	def __init__(self, job_queue, run_flag, system_state, state_lock, test_mode):
		# print("Job __init__()")
		super().__init__()


		self.normal_out_queue = job_queue
		self.run_flag         = run_flag
		self.system_state     = system_state
		self.state_lock       = state_lock
		self.test_mode        = test_mode


		self.last_rx = datetime.datetime.now()

		self.print_mod = 0


	def blocking_put_response(self, item):
		assert 'mode' in item, "Response items must have a mode key!"
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
			except socket.timeout:
				self.check_open_rpc_interface()
				return

			if tmp:
				assert 'mode' not in tmp, "No mode key allowed in rpc response!"

				nl   = tmp.get('extradat', {}).get('netloc', None)
				mode = tmp.get('extradat', {}).get('dispatch_mode', None)


				with acquire_timeout(self.state_lock, 10) as acquired:
					if acquired:
						self.system_state['active_jobs']     -= 1
						self.system_state['jobs_in']         += 1
						self.system_state['active_jobs']      = max(self.system_state['active_jobs'], 0)
						self.system_state['qsize']            = self.normal_out_queue.qsize()
						if nl:
							if mode and mode in self.system_state['ratelimiters']:
								self.log.info("Have mode in dispatched response: %s", mode)
								if 'success' in tmp and tmp['success']:
									self.system_state['ratelimiters'][mode].netloc_ok(nl)
								else:
									self.system_state['ratelimiters'][mode].netloc_error(nl)
							else:
								self.log.warning("Missing mode in dispatched response.")
								if 'success' in tmp and tmp['success']:
									for limiter in self.system_state['ratelimiters'].values():
										limiter.netloc_ok(nl)
								else:
									for limiter in self.system_state['ratelimiters'].values():
										limiter.netloc_error(nl)

						else:
							self.log.warning("Missing netloc in response extradat!")
					else:
						self.log.error("Failure acquiring lock when handling job response!")

				self.log.info("Job response received. Jobs in-flight: %s (qsize: %s)", self.system_state['active_jobs'], self.normal_out_queue.qsize())
				self.last_rx = datetime.datetime.now()

				tmp['mode'] = 'remote_fetch'
				self.blocking_put_response(tmp)
			else:

				with acquire_timeout(self.state_lock, 2) as acquired:
					if acquired:
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
			if self.normal_out_queue.qsize() > LOCAL_ENQUEUED_JOB_RESPONSES:
				self.log.warn("Long latency since last received job, but received job queue contains lots of jobs. Huh? (Jobqueue size: %s)", self.normal_out_queue.qsize())
			else:
				self.log.error("Timeout since last job seen. Resetting active job counter. (lastJob: %s)", self.last_rx + datetime.timedelta(minutes=NO_JOB_TIMEOUT_MINUTES))

				with acquire_timeout(self.state_lock, 10) as acquired:
					if acquired:
						self.system_state['active_jobs']     = 0
					else:
						self.log.error("Failure when resetting active jobs!")

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
			if self.test_mode:
				time.sleep(1)

				with acquire_timeout(self.state_lock, 10) as acquired:
					if acquired:
						self.system_state['active_jobs']      = 1
						self.system_state['jobs_in']         += 1
						self.system_state['active_jobs']      = 1
						self.system_state['qsize']            = 1
						for limiter in self.system_state['ratelimiters'].values():
							limiter.clear_active_counts(override_status=500)

			else:
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
		except KeyboardInterrupt:
			self.log.info("Saw keyboard interrupt. Breaking!")
			self.run_flag.value = 0
		except Exception:
			with open("error %s - %s.txt" % ('job_consumer', time.time()), "w") as fp:
				fp.write("Manager crashed?\n")
				fp.write(traceback.format_exc())
			raise



class RpcJobDispatcherInternal(LogBase.LoggerMixin, StatsdMixin.StatsdMixin, RpcMixin):

	statsd_prefix = 'ReadableWebProxy.Proc.JobDispatcher'
	loggerPath = "Main.JobDispatcher"



	def __init__(self, mode, job_queue, run_flag, system_state, state_lock, test_mode):
		# print("Job __init__()")
		self.loggerPath = "Main.JobDispatcher(%s)" % mode
		self.statsd_prefix = self.statsd_prefix + "." + mode
		super().__init__()
		self.mode = mode



		self.last_rx = datetime.datetime.now()


		self.db_interface = psycopg2.connect(
				database = settings.DATABASE_DB_NAME,
				user     = settings.DATABASE_USER,
				password = settings.DATABASE_PASS,
				host     = settings.DATABASE_IP,
			)

		# We need the job queue because the special case system can skip the rpc stuff entirely.
		self.normal_out_queue = job_queue

		self.system_state = system_state
		self.jq_mode      = mode
		self.run_flag     = run_flag
		self.state_lock   = state_lock
		self.test_mode    = test_mode

		self.ruleset        = WebMirror.rules.load_rules()
		self.specialcase    = WebMirror.rules.load_special_case_sites()
		self.triggerUrls    = set(WebMirror.rules.load_triggered_url_list())

		self.feed_urls_list = []
		for tmp in self.ruleset:
			if 'feedurls' in tmp and tmp['feedurls']:
				self.feed_urls_list.extend(tmp['feedurls'])

		self.feed_urls = set(self.feed_urls_list)

		self.rate_limit_skip = {}
		for rules in self.ruleset:
			for key, regex in rules['skip_filters']:
				assert key not in self.rate_limit_skip, "Multiple definition of skip filter for netloc '%s'" % key
				self.rate_limit_skip[key] = regex

		self.log.info("Have %s RSS feed URLS", len(self.feed_urls))
		self.log.info("Have %s netloc-filtered skip-limit regexes.", len(self.rate_limit_skip))

		self.print_mod = 0

		with state_lock:
			self.system_state['ratelimiters'][self.mode] = common.NetlocThrottler.NetlockThrottler(fifo_limit = 1000 * 1000)

	def blocking_put_response(self, item):
		assert 'mode' in item, "Response items must have a mode key!"
		while self.run_flag.value == 1:
			try:
				self.normal_out_queue.put_nowait(item)
				return
			except queue.Full:
				self.log.warning("Response queue full (%s items). Sleeping", self.normal_out_queue.qsize())
				time.sleep(1)


	def join_proc(self):
		self.log.info("Setting exit flag on processor.")
		self.run_flag.value = 0
		self.log.info("Joining on worker thread.")



	def put_job(self, raw_job):
		if self.test_mode:
			return

		# Recycle the rpc interface if it ded
		while 1:
			try:
				self.rpc_interface.put_job(raw_job)
				with acquire_timeout(self.state_lock, 10) as acquired:
					if acquired:
						self.system_state['active_jobs'] += 1
						self.system_state['jobs_out'] += 1
					else:
						self.log.error("Failure when updating active job counters!")

				self.log.info("Dispatched new job (active jobs: %s of %s, %s of %s)",
					self.system_state['active_jobs'], MAX_IN_FLIGHT_JOBS, self.system_state['qsize'], LOCAL_ENQUEUED_JOB_RESPONSES)
				return
			except TypeError:
				self.check_open_rpc_interface()
			except KeyError:
				self.check_open_rpc_interface()
			except socket.timeout:
				self.check_open_rpc_interface()
			except ConnectionRefusedError:
				self.check_open_rpc_interface()

	def put_fetch_job(self, jobid, joburl, netloc=None):
		# module='WebRequest', call='getItem'
		raw_job = WebMirror.JobUtils.buildjob(
			module         = 'WebRequest',
			call           = 'getItem',
			dispatchKey    = "fetcher",
			jobid          = jobid,
			args           = [joburl],
			kwargs         = {},
			additionalData = {
									'mode'          : 'fetch',
									'netloc'        : netloc,
									'dispatch_mode' : self.mode,
								},
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
		if netloc == "archiveofourown.org":
			return False

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

	def set_special_case_blocked(self, rid, joburl):
		self.log.warning("Setting job status to blocked for id->url: %s->'%s'", rid, joburl)
		cursor = self.db_interface.cursor()
		cursor.execute("""UPDATE web_pages         SET state='specialty_blocked' WHERE web_pages.id = %s;""", (rid, ))
		cursor.execute("""COMMIT;""")
		self.db_interface.commit()


	def fill_jobs(self):
		if 'drain' in sys.argv:
			return 0
		total_new = 0
		while self.system_state['active_jobs'] < MAX_IN_FLIGHT_JOBS and self.system_state['qsize'] < LOCAL_ENQUEUED_JOB_RESPONSES:
			old = self.system_state['active_jobs']
			with self.mon_con.pipeline() as pipe:
				with pipe.timer("get_task"):
					num_new = self._get_task_internal()
				with pipe.timer("get_deferred"):
					num_new += self._get_deferred_internal()
			self.log.info("Need to add jobs to the job queue (%s active, %s added)!", self.system_state['active_jobs'], self.system_state['active_jobs']-old)

			if self.run_flag.value != 1:
				return 0

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

		if not self.test_mode:
			self.check_open_rpc_interface()

		self.log.info("Job queue fetcher starting.")

		for _ in range(1000):
			if not self.run_flag.value == 1:
				break
			newj = self.fill_jobs()

			time.sleep(2.5)
			self.log.info("Job queue filler process. Added %s, active jobs: %s (out: %s, in: %s, pq: %s, deferred: %s). Runstate: %s",
				newj, self.system_state['active_jobs'], self.system_state['jobs_out'], self.system_state['jobs_in'], self.system_state['qsize'],
				self.system_state['ratelimiters'][self.mode].get_in_queues(), self.run_flag.value)

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

		new_j_l = []
		with acquire_timeout(self.state_lock, 2) as acquired:
			if acquired:
				new_j_l =self.system_state['ratelimiters'][self.mode].get_available_jobs()
			else:
				self.log.error("Failure when extracting jobs from rate-limiting system!")

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
							web_pages.state = 'new'::dlstate_enum
						AND
							normal_fetch_mode = true
						AND
							web_pages.file IS NULL
						AND
							web_pages.content IS NULL
						LIMIT {in_flight}
					)
				AND
					web_pages.state = 'new'::dlstate_enum
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
							web_pages.state = 'new'::dlstate_enum
						AND
							normal_fetch_mode = true
						LIMIT {in_flight}
					)
				AND
					web_pages.state = 'new'::dlstate_enum
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
							web_pages.state = 'new'::dlstate_enum
						AND
							normal_fetch_mode = true
						AND
							web_pages.priority < 9
							
						AND
							web_pages.distance < 1000000
						AND
							web_pages.ignoreuntiltime < now() + '5 minutes'::interval
						LIMIT {in_flight}
					)
				AND
					web_pages.state = 'new'::dlstate_enum
				RETURNING
					web_pages.id, web_pages.netloc, web_pages.url;
			'''.format(in_flight=min((MAX_IN_FLIGHT_JOBS, JOB_QUERY_CHUNK_SIZE)))
		'''
							(
							   SELECT
									4
									min(priority) + 3
								FROM
									web_pages
								WHERE
									state = 'new'::dlstate_enum
								AND
									normal_fetch_mode = true
								AND
									web_pages.ignoreuntiltime < now() + '5 minutes'::interval
							)
		'''

		start = time.time()

		while self.run_flag.value == 1:
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
				traceback.print_exc()
				self.log.warn("Error getting job (psycopg2.Error)! Delaying %s.", delay)
				time.sleep(delay)
				cursor.execute("ROLLBACK;")

		if self.run_flag.value != 1:
			return 0

		if not rids:
			self.log.warning("Query in mode %s returned no rows!", self.jq_mode)
			return 0

		rids = list(rids)
		# If we broke because a user-interrupt, we may not have a
		# valid rids at this point.
		if self.run_flag.value != 1:
			return 0

		xqtim = time.time() - start

		if not rids:
			self.log.warning("No jobs available! Sleeping for 5 seconds waiting for new jobs to become available!")
			for dummy_x in range(5):
				if self.run_flag.value == 1:
					time.sleep(1)
			return 0

		if xqtim > 0.5:
			self.log.error("Query execution time: %s ms. Fetched job IDs = %s", xqtim * 1000, len(rids))
		elif xqtim > 0.1:
			self.log.warn("Query execution time: %s ms. Fetched job IDs = %s", xqtim * 1000, len(rids))
		else:
			self.log.info("Query execution time: %s ms. Fetched job IDs = %s", xqtim * 1000, len(rids))

		processed = 0
		special_case = 0
		booksie = 0
		defer_count = 0
		del_count = 0
		immediate = 0
		defer = []
		for rid, netloc, joburl in rids:

			if netloc == "archiveofourown.org":
				# Do nothing, these are being handled by an out-of-process deletion interface
				del_count += 1

				continue

			processed += 1
			if "booksie.com" in netloc:
				booksie += 1
				print(netloc)
				continue

			if not self.outbound_job_wanted(netloc, joburl):
				del_count += 1
				self.delete_job(rid, joburl)

			elif WebMirror.SpecialCase.haveSpecialCase(self.specialcase, joburl, netloc):
				special_case += 1
				try:
					WebMirror.SpecialCase.pushSpecialCase(self.specialcase, rid, joburl, netloc, self)
				except WebMirror.SpecialCase.SpecialCaseFilterMissing:
					self.set_special_case_blocked(rid, joburl)
			else:
				# Do not route the rss fetches through the rate-limiting system.
				if joburl in self.feed_urls:
					immediate += 1
					self.log.info("Skipping fetch limiter due to feed URL")
					self.put_fetch_job(rid, joburl, netloc)
				elif netloc in self.rate_limit_skip and self.rate_limit_skip[netloc].search(joburl):
					immediate += 1
					self.log.info("Skipping fetch limiter due to rate_limit_skip for URL: '%s'", joburl)
					self.put_fetch_job(rid, joburl, netloc)
				else:
					defer_count += 1
					defer.append((rid, joburl, netloc))

		self.log.info("Of %s job IDs, %s were special-case, %s were rate-limited, %s were immediately dispatched, %s deleted, %s booksie (%s proc).",
				len(rids), special_case, defer_count, immediate, del_count, booksie, processed)


		with acquire_timeout(self.state_lock, 10) as acquired:
			if acquired:
				for rid_d, joburl_d, netloc_d in defer:
					self.system_state['ratelimiters'][self.mode].put_job(rid_d, joburl_d, netloc_d)
			else:
				self.log.error("Failed to acquire rate-limiter synchronization lock!")
		cursor.close()

		if not rids:
			self.log.warning("No jobs to dispatch in query response!?")


		# Deleted and defered jobs don't count towards the active jobs number.
		return len(rids) - (del_count + defer_count)


	def run(self):
		try:
			self.queue_filler_proc()
		except KeyboardInterrupt:
			self.log.info("Saw keyboard interrupt. Breaking!")
			self.run_flag.value = 0
		except Exception:
			with open("error %s - %s.txt" % (self.jq_mode, time.time()), "w") as fp:
				fp.write("Manager crashed?\n")
				fp.write(traceback.format_exc())
			raise


class MultiRpcRunner(LogBase.LoggerMixin, StatsdMixin.StatsdMixin):
	loggerPath = "Main.MultiRpcRunner"
	statsd_prefix = 'ReadableWebProxy.Proc.DispatcherManager'


	def __init__(self, job_queue, run_flag, test_mode):
		super().__init__()

		self.log.info("MultiRpcRunner creating RPC feeder/consumer threads")
		self.job_queue = job_queue
		self.run_flag  = run_flag
		self.test_mode = test_mode

		self.state_lock = threading.Lock()

	def update_stats(self, statedict, threads):
		with self.mon_con.pipeline() as pipe:
			with acquire_timeout(self.state_lock, 10) as acquired:
				if acquired:
					pipe.gauge('active_jobs', statedict['active_jobs'])
					pipe.gauge('jobs_out',    statedict['jobs_out'   ])
					pipe.gauge('jobs_in',     statedict['jobs_in'    ])
					pipe.gauge('qsize',       statedict['qsize'      ])



		self.log.info("Queue stats: active: %s, out: %s, in: %s, qsize: %s",
				statedict['active_jobs'],
				statedict['jobs_out'   ],
				statedict['jobs_in'    ],
				statedict['qsize'      ]
			)

		self.log.info("Thread States: %s",
				{
					int(thread.ident) : thread.is_alive()
					for thread in threads
				}
			)


	def run(self):

		system_state = {
			'active_jobs'  : 0,
			'jobs_out'     : 0,
			'jobs_in'      : 0,
			'qsize'        : 0,
			'ratelimiters' : {},

		}



		threads = [
			threading.Thread(target=RpcJobDispatcherInternal('priority',   self.job_queue, self.run_flag, system_state, state_lock=self.state_lock, test_mode=self.test_mode).run),
			# threading.Thread(target=RpcJobDispatcherInternal('new_fetch',  self.job_queue, self.run_flag, system_state, state_lock=self.state_lock, test_mode=self.test_mode).run),
			# threading.Thread(target=RpcJobDispatcherInternal('random',     self.job_queue, self.run_flag, system_state, state_lock=self.state_lock, test_mode=self.test_mode).run),
			threading.Thread(target=RpcJobConsumerInternal(                self.job_queue, self.run_flag, system_state, state_lock=self.state_lock, test_mode=self.test_mode).run),
		]

		self.log.info("MultiRpcRunner starting RPC feeder/consumer threads")
		for thread in threads:
			thread.start()

		self.log.info("MultiRpcRunner threads started")

		last_reduce     =  0
		reduce_interval = 3

		while self.run_flag.value == 1:
			for _ in range(10):
				if not self.test_mode:
					self.update_stats(system_state, threads)
				time.sleep(1)
				if not self.run_flag.value == 1:
					break
			self.log.info("Active dispatchers: %s", [tmp.is_alive() for tmp in threads])



			# Every 90 seconds, we deincrement the active jobs counts.
			last_reduce += 1

			self.log.info("Job reduce step: %s of %s.", last_reduce, reduce_interval)
			if last_reduce > reduce_interval:
				last_reduce = 0
				with acquire_timeout(self.state_lock, 10) as acquired:
					if acquired:
						self.log.info("Calling job reducer!")
						for limiter in system_state['ratelimiters'].values():
							limiter.job_reduce()
						for mode, limiter in system_state['ratelimiters'].items():
							self.log.info("Limiter for %s -> %s", mode, limiter.get_in_queues())



		self.log.info("MultiRpcRunner exit flag seen. Joining on threads")
		while any([tmp.is_alive() for tmp in threads]):
			for thread in [tmp for tmp in threads if tmp.is_alive()]:
				try:
					thread.join(timeout=1)
				except multiprocessing.TimeoutError:
					self.log.error("Joining %s failed!", thread)
		self.log.info("MultiRpcRunner joined all threads. Exiting")



	@classmethod
	def run_shim(cls, job_queue, run_flag, test_mode):

		try:
			instance = cls(job_queue, run_flag, test_mode=test_mode)
			instance.run()

		except KeyboardInterrupt:
			print("Saw keyboard interrupt. Breaking!")
			run_flag.value = 0

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


	def __init__(self, start_worker=True, test_mode=False):
		super().__init__()

		self.log.info("Launching job-dispatching RPC system")

		# This queue has to be a multiprocessing queue, because it's shared across multiple processes.
		self.normal_out_queue  = multiprocessing.Queue(maxsize=MAX_IN_FLIGHT_JOBS * 2)

		self.run_flag = multiprocessing.Value("i", 1, lock=False)

		if start_worker:
			self.main_job_agg = multiprocessing.Process(target=MultiRpcRunner.run_shim, args=(self.normal_out_queue, self.run_flag), kwargs={"test_mode" : test_mode})
			self.main_job_agg.start()
		else:
			self.main_job_agg = None


	def get_queues(self):
		return self.normal_out_queue

	def join_proc(self):
		self.log.info("Requesting job-dispatching RPC system to halt.")
		self.run_flag.value = 0

		# We have to consume any remaining jobs in the output queue, or we'll never
		# fully exit.
		if self.main_job_agg:
			for _ in range(60 * 5):
				try:
					self.main_job_agg.join(timeout=1)
					return

				except multiprocessing.TimeoutError:
					pass

				self.log.info("Waiting for job dispatcher to join. Currently active jobs in queue: %s",
						self.normal_out_queue.qsize()
					)

			while True:
				self.main_job_agg.join(timeout=1)
				try:
					self.main_job_agg.join(timeout=1)
					return

				except multiprocessing.TimeoutError:
					pass

				self.log.error("Timeout when waiting for join. Bulk consuming from intermediate queue.")
				try:
					while 1:
						self.normal_out_queue.get_nowait()
				except queue.Empty:
					pass



	def get_status(self):
		if self.main_job_agg:
			return "Worker: %s, alive: %s, exit-code: %s" % (
				self.main_job_agg.pid, self.main_job_agg.is_alive(), self.main_job_agg.exitcode)

		return "Worker is none! Error!"


def test():
	print("Wat?")

	import logSetup
	logSetup.initLogging()


	tester = RpcJobManagerWrapper(test_mode=True)

	while True:
		time.sleep(1)



if __name__ == "__main__":
	test()

