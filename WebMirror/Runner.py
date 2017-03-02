
import time
import os
import multiprocessing
import signal
import logging
import logSetup
import cProfile
import traceback
import threading
import sys
import queue

import cachetools

# from pympler.tracker import SummaryTracker, summary, muppy
# import tracemalloc

import sqlalchemy.exc
from sqlalchemy.sql import text
from sqlalchemy.sql import func
import psycopg2


if __name__ == "__main__":
	logSetup.initLogging()

import config
import runStatus

import WebMirror.Engine
import WebMirror.rules
import common.util.urlFuncs as urlFuncs
import common.database as db
import WebMirror.NewJobQueue as njq

import common.stuck

import common.get_rpyc

class RunInstance(object):
	def __init__(self, num, response_queue, new_job_queue, cookie_lock, nosig=True):
		# print("RunInstance %s init!" % num)
		if nosig:
			# signal.signal(signal.SIGINT, handler)
			signal.signal(signal.SIGINT, signal.SIG_IGN)
		self.num = num
		self.log = logging.getLogger("Main.Text.Web")
		self.resp_queue    = response_queue
		self.cookie_lock   = cookie_lock
		self.new_job_queue = new_job_queue

		# print("RunInstance %s MOAR init!" % num)

	def __del__(self):
		db.delete_db_session()

	def do_task(self):

		db_handle = db.get_db_session()

		hadjob = False
		try:
			self.archiver = WebMirror.Engine.SiteArchiver(self.cookie_lock, new_job_queue=self.new_job_queue, response_queue=self.resp_queue, db_interface=db_handle)
			hadjob = self.archiver.taskProcess()
		finally:
			# Clear out the sqlalchemy state
			db_handle.expunge_all()
			db.delete_db_session()

		return hadjob

	def go(self):

		self.log.info("RunInstance starting!")
		loop = 0
		# We have to only let the child threads run for a period of time, or something
		# somewhere in sqlalchemy appears to be leaking memory.
		for dummy_x in range(50):

			if runStatus.run_state.value == 1:
				# objgraph.show_growth(limit=3)
				hadjob = self.do_task()
			else:
				self.log.info("Thread %s exiting.", self.num)
				break
			loop += 1

			# If there was nothing to do, sleep 30 seconds and recheck.
			# This is because with 50 workers with a sleep-time of 5 seconds on job-miss,
			# it was causing 100% CPU usage on the DB just for the getjob queries. (I think)
			if not hadjob:
				sleeptime = 10
				self.log.info("Nothing for thread %s to do. Sleeping %s seconds.", self.num, sleeptime)
				for _x in range(sleeptime):
					time.sleep(1)
					if runStatus.run_state.value != 1:
						self.log.info("Thread %s saw exit flag while waiting for jobs. Runstate: %s", self.num, runStatus.run_state.value)
						return

		if runStatus.run_state.value:
			self.log.info("Thread %s restarting. Runstate: %s", self.num, runStatus.run_state.value)
		else:
			self.log.info("Thread %s halting. Runstate: %s", self.num, runStatus.run_state.value)




	@classmethod
	def run_prof(cls, num, total_worker_count, worker_num, response_queue, new_job_queue, cookie_lock, nosig=True):

		pid = os.getpid()
		try:
			cProfile.runctx('cls.run(num, response_queue, new_job_queue, cookie_lock, nosig)', globals(), locals(), 'prof%d.prof' % pid)
		except Exception as e:
			print("Wat?")
			print("Wat?")
			print("Wat?")
			print("Wat?")
			print("Wat?")
			print("Wat?")
			print("Wat?")
			traceback.print_exc()
			raise e

	@classmethod
	def run(cls, num, total_worker_count, worker_num, response_queue, new_job_queue, cookie_lock, nosig=True):
		logSetup.resetLoggingLocks()
		common.stuck.install_pystuck()

		# total_worker_count, worker_num are ignored at the moment.

		try:
			run = cls(num, response_queue, new_job_queue, cookie_lock, nosig)
			# print("Class instantiated: ", run)
			run.go()
		except Exception:
			print()
			print("Exception in sub-process!")
			traceback.print_exc()

def initializeStartUrls(rules):
	print("Initializing all start URLs in the database")
	sess = db.get_db_session()
	for ruleset in [rset for rset in rules if rset['starturls']]:
		for starturl in ruleset['starturls']:
			have = sess.query(db.WebPages) \
				.filter(db.WebPages.url == starturl)   \
				.count()
			if not have:
				netloc = urlFuncs.getNetLoc(starturl)
				new = db.WebPages(
						url               = starturl,
						starturl          = starturl,
						netloc            = netloc,
						type              = ruleset['type'],
						priority          = db.DB_IDLE_PRIORITY,
						distance          = db.DB_DEFAULT_DIST,
						normal_fetch_mode = ruleset['normal_fetch_mode'],
					)
				print("Missing start-url for address: '{}'".format(starturl))
				sess.add(new)
			try:
				sess.commit()
			except sqlalchemy.SQLAlchemyError:
				print("Failure inserting start url for address: '{}'".format(starturl))

				sess.rollback()
	sess.close()
	db.delete_db_session()

def resetInProgress():
	print("Resetting any stalled downloads from the previous session.")

	sess = db.get_db_session()
	sess.query(db.WebPages) \
		.filter(
				(db.WebPages.state == "fetching")           |
				(db.WebPages.state == "processing")         |
				(db.WebPages.state == "specialty_deferred") |
				(db.WebPages.state == "specialty_ready")
				)   \
		.update({db.WebPages.state : "new"})
	sess.commit()
	sess.close()
	db.delete_db_session()

class UpdateAggregator(object):
	def __init__(self, msg_queue, db_interface):
		self.queue = msg_queue
		self.log = logging.getLogger("Main.Agg.Manager")

		try:
			signal.signal(signal.SIGINT, signal.SIG_IGN)
		except ValueError:
			self.log.warning("Cannot configure job fetcher task to ignore SIGINT. May be an issue.")

		# LRU Cache with a maxsize of 1 million, and a TTL of 6 hours
		self.seen = cachetools.TTLCache(maxsize=1000 * 1000, ttl=60 * 60 * 6)

		self.links = 0
		self.amqpUpdateCount = 0
		self.deathCounter = 0

		self.batched_links = []

		self.db_int = db_interface

	def check_init_func(self):
		raw_cur = self.db_int.connection().connection.cursor()

		cmd = """
			CREATE OR REPLACE FUNCTION upsert_link(
			        url_v text,
			        starturl_v text,
			        netloc_v text,
			        distance_v integer,
			        is_text_v boolean,
			        priority_v integer,
			        type_v itemtype_enum,
			        addtime_v timestamp without time zone,
			        state_v dlstate_enum,
			        ignoreuntiltime_v timestamp without time zone
			        )
			    RETURNS VOID AS $$

			    INSERT INTO
			        web_pages
			         (url, starturl, netloc, distance, is_text, priority, type, addtime, state)
			    VALUES
			        (url_v, starturl_v, netloc_v, distance_v, is_text_v, priority_v, type_v, addtime_v, state_v)
			    ON CONFLICT (url) DO
			        UPDATE
			            SET
			                state           = EXCLUDED.state,
			                starturl        = EXCLUDED.starturl,
			                netloc          = EXCLUDED.netloc,
			                is_text         = EXCLUDED.is_text,
			                distance        = LEAST(EXCLUDED.distance, web_pages.distance),
			                priority        = GREATEST(EXCLUDED.priority, web_pages.priority),
			                addtime         = LEAST(EXCLUDED.addtime, web_pages.addtime)
			            WHERE
			            (
			                    web_pages.ignoreuntiltime < ignoreuntiltime_v
			                AND
			                    web_pages.url = EXCLUDED.url
			                AND
			                    (web_pages.state = 'complete' OR web_pages.state = 'error')
			            )
			        ;

			$$ LANGUAGE SQL;

		"""
		raw_cur.execute(cmd)
		raw_cur.execute("COMMIT;")

	def check_open_rpc_interface(self):
		try:
			if self.rpc_interface.check_ok():
				return


		except Exception:
			try:
				self.rpc_interface.close()
			except Exception:
				pass
			self.rpc_interface = common.get_rpyc.RemoteJobInterface("FeedUpdater")


	def do_amqp(self, pkt):
		self.amqpUpdateCount += 1

		if self.amqpUpdateCount % 50 == 0:
			self.log.info("Transmitted AMQP messages: %s", self.amqpUpdateCount)

		if config.C_DO_RABBIT:
			self.check_open_rpc_interface()
			self.rpc_interface.put_feed_job(pkt)


	def do_link_batch_update(self):
		if not self.batched_links:
			return
		self.log.info("Inserting %s items into DB in batch.", len(self.batched_links))


		raw_cur = self.db_int.connection().connection.cursor()

		#  Fucking huzzah for ON CONFLICT!
		cmd = """
			INSERT INTO
			    web_pages
			    (url, starturl, netloc, distance, is_text, priority, type, addtime, state)
			VALUES
			    (%(url_{cnt})s, %(starturl_{cnt})s, %(netloc_{cnt})s, %(distance_{cnt})s, %(is_text_{cnt})s, %(priority_{cnt})s, %(type_{cnt})s, %(addtime_{cnt})s, %(state_{cnt})s)
			ON CONFLICT (url) DO
			    UPDATE
			        SET
			            state           = EXCLUDED.state,
			            starturl        = EXCLUDED.starturl,
			            netloc          = EXCLUDED.netloc,
			            is_text         = EXCLUDED.is_text,
			            distance        = LEAST(EXCLUDED.distance, web_pages.distance),
			            priority        = GREATEST(EXCLUDED.priority, web_pages.priority),
			            addtime         = LEAST(EXCLUDED.addtime, web_pages.addtime)
			        WHERE
			        (
			                web_pages.ignoreuntiltime < %(ignoreuntiltime_{cnt})s
			            AND
			                web_pages.url = EXCLUDED.url
			            AND
			                (web_pages.state = 'complete' OR web_pages.state = 'error')
			        )
			    ;
				""".replace("	", " ").replace("\n", " ")

		per_cmd = """
			INSERT INTO
			    web_pages
			    (url, starturl, netloc, distance, is_text, priority, type, addtime, state)
			VALUES
			    (%(url)s, %(starturl)s, %(netloc)s, %(distance)s, %(is_text)s, %(priority)s, %(type)s, %(addtime)s, %(state)s)
			ON CONFLICT (url) DO
			    UPDATE
			        SET
			            state           = EXCLUDED.state,
			            starturl        = EXCLUDED.starturl,
			            netloc          = EXCLUDED.netloc,
			            is_text         = EXCLUDED.is_text,
			            distance        = LEAST(EXCLUDED.distance, web_pages.distance),
			            priority        = GREATEST(EXCLUDED.priority, web_pages.priority),
			            addtime         = LEAST(EXCLUDED.addtime, web_pages.addtime)
			        WHERE
			        (
			                web_pages.ignoreuntiltime < %(ignoreuntiltime)s
			            AND
			                web_pages.url = EXCLUDED.url
			            AND
			                (web_pages.state = 'complete' OR web_pages.state = 'error')
			        )
			    ;
				""".replace("	", " ").replace("\n", " ")

		while "  " in per_cmd:
			per_cmd = per_cmd.replace("  ", " ")
		while "  " in cmd:
			cmd = cmd.replace("  ", " ")




		cmds = [cmd.format(cnt=cnt) for cnt in range(len(self.batched_links))]
		bulk_cmd = " ".join(cmds)

		# Build a nested list of dicts
		bulk_dict = [ {key+"_{cnt}".format(cnt=cnt) : val for key, val in self.batched_links[cnt].items()} for cnt in range(len(self.batched_links)) ]

		# Then flatten it down to a single dict
		bulk_dict = {k: v for d in bulk_dict for k, v in d.items()}

		# We use a statement timeout context of 5000 ms, so we don't get wedged on a lock.
		raw_cur.execute("SET statement_timeout TO 5000;")

		raw_cur.execute("BEGIN;")
		try:
			raw_cur.execute(bulk_cmd, bulk_dict)
			raw_cur.execute("COMMIT;")
			raw_cur.execute("RESET statement_timeout;")
			self.batched_links = []
			return

		except psycopg2.Error:
			self.log.error("psycopg2.Error - Failure on bulk insert.")
			raw_cur.execute("ROLLBACK;")


		# Only commit per-URL if we're tried to do the update in batch, and failed.
		commit_each = False
		while 1:
			try:
				raw_cur.execute("BEGIN;")
				for paramset in self.batched_links:
					assert isinstance(paramset['starturl'], str)
					if len(paramset['url']) > 2000:
						self.log.error("URL Is too long to insert into the database!")
						self.log.error("URL: '%s'", paramset['url'])

					else:
						# Forward-data the next walk, time, rather then using now-value for the thresh.
						raw_cur.execute(per_cmd, paramset)
						if commit_each:
							raw_cur.execute("COMMIT;")
							raw_cur.execute("BEGIN;")

				raw_cur.execute("COMMIT;")
				break

			except psycopg2.Error:
				if commit_each is False:
					self.log.warning("psycopg2.Error - Retrying with commit each.")
				else:
					self.log.warning("psycopg2.Error - Retrying.")
					traceback.print_exc()

				raw_cur.execute("ROLLBACK;")
				commit_each = True

		raw_cur.execute("RESET statement_timeout;")

		self.batched_links = []


	def do_link(self, linkdict):

		assert 'url'             in linkdict
		assert 'starturl'        in linkdict
		assert 'netloc'          in linkdict
		assert 'distance'        in linkdict
		assert 'is_text'         in linkdict
		assert 'priority'        in linkdict
		assert 'type'            in linkdict
		assert 'state'           in linkdict
		assert 'addtime'         in linkdict
		assert 'ignoreuntiltime' in linkdict

		url = linkdict['url']

		# Only allow items through if they're not in the LRU cache, or have not been upserted
		# in the last 6 hours
		if url in self.seen:
			# Fucking huzzah for ON CONFLICT!
			self.batched_links.append(linkdict)
			# Kick item up to the top of the LRU list
			self.seen[url] = True

			if len(self.batched_links) >= 500:
				self.do_link_batch_update()
		# else:
		# 	self.log.info("Skipping upserting: '%s'", url)

	def do_task(self):

		target, value = self.queue.get_nowait()

		if (self.links % 50) == 0:
			self.log.info("Aggregator active. Total cached URLs: %s, Items in processing queue: %s, transmitted release messages: %s.", self.seen.currsize, self.queue.qsize(), self.amqpUpdateCount)

		self.links += 1

		if target == "amqp_msg":
			if config.C_DO_RABBIT:
				self.do_amqp(value)
		elif target == "new_link":
			self.do_link(value)
		else:
			print("Todo", target, value)

	def run(self):

		while 1:
			try:
				while 1:
					# print("Loopin!")
					self.do_task()
					self.deathCounter = 0
			except queue.Empty:
				if runStatus.agg_run_state.value != 1:

					self.deathCounter += 1
					time.sleep(0.1)
					if self.deathCounter > 5:
						self.log.info("Aggregator thread exiting.")
						break
			except Exception:
				self.log.error("Exception in aggregator!")
				for line in traceback.format_exc().split("\n"):
					self.log.error(line.rstrip())
			# Fffffuuuuu time.sleep barfs on KeyboardInterrupt
			try:
				time.sleep(1)
				self.do_link_batch_update()
			except KeyboardInterrupt:
				pass

		self.do_link_batch_update()

	def close(self):
		if config.C_DO_RABBIT:
			self.log.info("Aggregator thread closing interface.")
			# self._amqpint.close()

	@classmethod
	def launch_agg(cls, agg_queue):

		try:
			common.stuck.install_pystuck()
			agg_db = db.get_db_session()
			instance = cls(agg_queue, agg_db)
			instance.run()
			instance.close()
		except Exception as e:
			import traceback
			print()
			print()
			print()
			print()
			print()
			print()
			print("Aggregator exception!")
			traceback.print_exc()



if __name__ == "__main__":
	runner = Crawler()
	runner.run()
	print(runner)

