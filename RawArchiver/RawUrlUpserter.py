

import os
import datetime
import cProfile
import traceback
import pprint
import threading
import urllib.parse
import sys
import queue

import cachetools
import tqdm

# from pympler.tracker import SummaryTracker, summary, muppy
# import tracemalloc

import sqlalchemy.exc
from sqlalchemy.sql import text
from sqlalchemy.sql import func


if '__pypy__' in sys.builtin_module_names:
	import psycopg2cffi as psycopg2
else:
	import psycopg2


import config
import runStatus
import concurrent.futures

import common.util.urlFuncs as urlFuncs
import common.util.misc as misc
import common.util.psycopg_execute_batch as psycopg_execute_batch
import common.database as db
import common.stuck
import common.get_rpyc

import sqlalchemy.exc
from sqlalchemy.sql import text
from sqlalchemy.sql import func


import runStatus
import concurrent.futures

import common.util.urlFuncs as urlFuncs
import common.database as db

import common.stuck

import common.get_rpyc
import RawArchiver.RawActiveModules



def initializeRawStartUrls():
	print("Initializing all start URLs in the database")
	sess = common.database.get_db_session()
	for module in RawArchiver.RawActiveModules.ACTIVE_MODULES:
		for starturl in module.get_start_urls():
			have = sess.query(common.database.RawWebPages) \
				.filter(common.database.RawWebPages.url == starturl)   \
				.count()
			if not have:
				netloc = urlFuncs.getNetLoc(starturl)
				new = common.database.RawWebPages(
						url               = starturl,
						starturl          = starturl,
						netloc            = netloc,
						priority          = common.database.DB_IDLE_PRIORITY,
						distance          = common.database.DB_DEFAULT_DIST,
					)
				print("Missing start-url for address: '{}'".format(starturl))
				sess.add(new)
			try:
				sess.commit()
			except Exception:
				print("Failure inserting start url for address: '{}'".format(starturl))

				sess.rollback()
	sess.close()
	common.database.delete_db_session()


def resetRawInProgress():
	print("Resetting any stalled downloads from the previous session.")

	sess = db.get_db_session()

	commit_interval =  50000
	step            =  50000

	with db.session_context() as sess:
		try:
			# sess.execute('''SET enable_bitmapscan TO off;''')
			print("Getting minimum row in need or update..")
			start = sess.execute("""SELECT min(id) FROM raw_web_pages WHERE state = 'fetching' OR state = 'processing'""")
			# start = sess.execute("""SELECT min(id) FROM raw_web_pages WHERE state = 'fetching' OR state = 'processing' OR state = 'specialty_deferred' OR state = 'specialty_ready'""")
			start = list(start)[0][0]
			if start is None:
				print("No rows to reset!")
				return
			print("Minimum row ID:", start, "getting maximum row...")
			stop = sess.execute("""SELECT max(id) FROM raw_web_pages WHERE state = 'fetching' OR state = 'processing'""")
			# stop = sess.execute("""SELECT max(id) FROM raw_web_pages WHERE state = 'fetching' OR state = 'processing' OR state = 'specialty_deferred' OR state = 'specialty_ready'""")
			stop = list(stop)[0][0]
			print("Maximum row ID: ", stop)


			print("Need to fix rows from %s to %s" % (start, stop))
			start = start - (start % step)

			changed = 0
			tot_changed = 0
			for idx in tqdm.tqdm(range(start, stop, step), desc="Resetting raw URLs"):
				try:
					# SQL String munging! I'm a bad person!
					# Only done because I can't easily find how to make sqlalchemy
					# bind parameters ignore the postgres specific cast
					# The id range forces the query planner to use a much smarter approach which is much more performant for small numbers of updates
					have = sess.execute("""UPDATE
												raw_web_pages
											SET
												state = 'new'
											WHERE
												(state = 'fetching' OR state = 'processing')
											AND
												id > {}
											AND
												id <= {};""".format(idx, idx+step))
					# print()

					# processed  = idx - start
					# total_todo = stop - start
					# print('\r%10i, %10i, %7.4f, %6i, %8i\r' % (idx, stop, processed/total_todo * 100, have.rowcount, tot_changed), end="", flush=True)
					changed += have.rowcount
					tot_changed += have.rowcount
					if changed > commit_interval:
						print("Committing (%s changed rows)...." % changed, end=' ')
						sess.commit()
						print("done")
						changed = 0

				except sqlalchemy.exc.OperationalError:
					sess.rollback()
				except sqlalchemy.exc.InvalidRequestError:
					sess.rollback()


			sess.commit()

		finally:
			pass
			# sess.execute('''SET enable_bitmapscan TO on;''')

	db.delete_db_session()


# LRU Cache with a maxsize of 1 million, and a TTL of 6 hours
SEEN_CACHE = cachetools.TTLCache(maxsize=100 * 1000, ttl=60 * 60 * 6)


def links_to_dicts(links_in, starturl, distance, priority):
	ret = []

	for link in links_in:

		if link in SEEN_CACHE:
			continue

		SEEN_CACHE[link] = True

		# print("Doing insert", commit_each, link)
		start = urllib.parse.urlsplit(link).netloc

		assert link.startswith("http"), "Link %s doesn't seem to be HTTP content?" % link
		assert start

		data = {
			'url'             : link,
			'starturl'        : starturl,
			'netloc'          : start,
			'distance'        : distance,
			'priority'        : priority,
			'state'           : "new",
			'addtime'         : datetime.datetime.now(),

			# Don't retrigger unless the ignore time has elaped.
			'ignoreuntiltime' : datetime.datetime.now(),
			}

		ret.append(data)
	return ret

def do_link_batch_update_sess(logger, interface, link_batch):
	if not link_batch:
		return

	expected_keys = set([
			'url',
			'starturl',
			'netloc',
			'distance',
			'priority',
			'state',
			'addtime',
			'ignoreuntiltime',
		])


	for item in link_batch:
		try:
			assert 'url'              in item
			assert 'starturl'         in item
			assert 'netloc'           in item
			assert 'distance'         in item
			assert 'priority'         in item
			assert 'state'            in item
			assert 'addtime'          in item
			assert 'ignoreuntiltime'  in item

		except AssertionError:
			logger.error("Missing key from raw entry: ")
			item_str = pprint.pformat(item)
			for line in item_str.split("\n"):
				logger.error("	%s", line.rstrip())
			raise

		item_keys = set(item.keys())
		excess_keys = item_keys - expected_keys
		try:
			assert not excess_keys
		except AssertionError:
			logger.error("Excess key(s) in raw entry: '%s'", excess_keys)
			item_str = pprint.pformat(item)
			for line in item_str.split("\n"):
				logger.error("	%s", line.rstrip())
			raise


	logger.info("Inserting %s items into DB in batch.", len(link_batch))
	# This is kind of horrible.
	# Reach down through sqlalchemy and pull out the raw cursor directly.
	raw_cur = interface.connection().connection.cursor()

	per_cmd = """
	SELECT upsert_link_raw(
			%(url)s,
			%(starturl)s,
			%(netloc)s,
			%(distance)s,
			%(priority)s,
			%(addtime)s,
			%(state)s,
			%(ignoreuntiltime)s
			);
			""".replace("	", " ")

	per_cmd = per_cmd.replace("\n", " ")

	while "  " in per_cmd:
		per_cmd = per_cmd.replace("  ", " ")

	# Somehow we're getting here with an open transaction. I have no idea what's opening them.
	# Something something DBAPI
	raw_cur.execute("COMMIT;")


	rowcnt = 0
	try:
		for subc in misc.batch(link_batch, 50):
			# We don't care about isolation for these operations, as each operation
			# is functionally independent.
			raw_cur.execute("BEGIN TRANSACTION ISOLATION LEVEL READ COMMITTED;")

			# We use a statement timeout context of 2500 ms, so we don't get wedged on a lock.
			raw_cur.execute("SET statement_timeout TO 2500;")

			# We try the bulk insert command first.
			psycopg_execute_batch.execute_batch(raw_cur, per_cmd, subc)
			rowcnt += raw_cur.rowcount
			raw_cur.execute("COMMIT;")
			raw_cur.execute("RESET statement_timeout;")
		link_batch = []
		logger.info("Touched AT LEAST %s rows", rowcnt)
		return rowcnt

	except psycopg2.Error:
		logger.error("psycopg2.Error - Failure on bulk insert.")
		for line in traceback.format_exc().split("\n"):
			logger.error(line)
		raw_cur.execute("ROLLBACK;")
		logger.error("Retrying.")

	rowcnt = 0
	try:
		for subc in misc.batch(link_batch, 5):
			# We don't care about isolation for these operations, as each operation
			# is functionally independent.
			raw_cur.execute("BEGIN TRANSACTION ISOLATION LEVEL READ COMMITTED;")

			# We use a statement timeout context of 2500 ms, so we don't get wedged on a lock.
			raw_cur.execute("SET statement_timeout TO 2500;")

			# We try the bulk insert command first.
			psycopg_execute_batch.execute_batch(raw_cur, per_cmd, subc)
			rowcnt += raw_cur.rowcount
			raw_cur.execute("COMMIT;")
			raw_cur.execute("RESET statement_timeout;")
		link_batch = []
		logger.info("Touched AT LEAST %s rows", rowcnt)
		return rowcnt

	except psycopg2.Error:
		logger.error("psycopg2.Error - Failure on bulk insert.")
		for line in traceback.format_exc().split("\n"):
			logger.error(line)
		raw_cur.execute("ROLLBACK;")
		logger.error("Retrying with per upsert commit.")

	# If the bulk insert failed, we then try a per-URL upsert
	# We only commit per-URL if we're tried to do per-URL update in batch, and failed.
	commit_each = False
	while 1:
		rowcnt = 0
		try:
			raw_cur.execute("BEGIN TRANSACTION ISOLATION LEVEL READ COMMITTED;")

			# We use a statement timeout context of 2500 ms, so we don't get wedged on a lock.
			raw_cur.execute("SET statement_timeout TO 2500;")

			for paramset in link_batch:
				assert isinstance(paramset['starturl'], str)
				if len(paramset['url']) > 2000:
					logger.error("URL Is too long to insert into the database!")
					logger.error("URL: '%s'", paramset['url'])

				else:
					# Forward-data the next walk, time, rather then using now-value for the thresh.
					raw_cur.execute(per_cmd, paramset)
					rowcnt += raw_cur.rowcount

					if commit_each:
						raw_cur.execute("COMMIT;")
						raw_cur.execute("BEGIN TRANSACTION ISOLATION LEVEL READ COMMITTED;")
						# We use a statement timeout context of 2500 ms, so we don't get wedged on a lock.
						raw_cur.execute("SET statement_timeout TO 2500;")

			raw_cur.execute("COMMIT;")
			break

		except psycopg2.Error:
			if commit_each is False:
				logger.warning("psycopg2.Error - Retrying with commit each.")
			else:
				logger.warning("psycopg2.Error - Retrying.")
				traceback.print_exc()

			raw_cur.execute("ROLLBACK;")
			commit_each = True

	raw_cur.execute("RESET statement_timeout;")

	logger.info("Changed %s rows", rowcnt)

	return

def check_init_func():
	with db.session_context() as sess:
		raw_cur = sess.connection().connection.cursor()

		cmd = """
			CREATE OR REPLACE FUNCTION upsert_link_raw(
					url_v text,
					starturl_v text,
					netloc_v text,
					distance_v integer,
					priority_v integer,
					addtime_v timestamp without time zone,
					state_v dlstate_enum,
					ignoreuntiltime_v timestamp without time zone
					)
				RETURNS VOID AS $$

				INSERT INTO
					raw_web_pages
					(url, starturl, netloc, distance, priority, addtime, state, ignoreuntiltime)
				-- 	 (url, starturl, netloc, distance, priority, addtime, state, ignoreuntiltime)
				VALUES
					(     url_v,   starturl_v,   netloc_v,   distance_v,   priority_v,   addtime_v,   state_v, ignoreuntiltime_v)
				ON CONFLICT (url) DO
					UPDATE
						SET
							state           = EXCLUDED.state,
							starturl        = EXCLUDED.starturl,
							netloc          = EXCLUDED.netloc,
							-- Largest distance is 100, but it's not checked
							distance        = LEAST(EXCLUDED.distance, raw_web_pages.distance),
							-- The lowest priority is 10.
							priority        = LEAST(GREATEST(EXCLUDED.priority, raw_web_pages.priority), 10),
							addtime         = LEAST(EXCLUDED.addtime, raw_web_pages.addtime)
						WHERE
						(
								raw_web_pages.ignoreuntiltime < ignoreuntiltime_v
							AND
								raw_web_pages.url = EXCLUDED.url
							AND
								(raw_web_pages.state = 'complete' OR raw_web_pages.state = 'error')
						)
					;

			$$ LANGUAGE SQL;

		"""
		raw_cur.execute(cmd)
		raw_cur.execute("COMMIT;")
