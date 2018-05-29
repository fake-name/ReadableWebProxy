

import time
import os
import multiprocessing
import signal
import logging
import logSetup
import cProfile
import traceback
import tqdm
import threading
import sys
import queue

import cachetools

# from pympler.tracker import SummaryTracker, summary, muppy
# import tracemalloc

import sqlalchemy.exc
from sqlalchemy.sql import text
from sqlalchemy.sql import func


import config
import runStatus
import concurrent.futures

import WebMirror.Engine
import WebMirror.rules
import common.util.urlFuncs as urlFuncs
import common.database as db
import WebMirror.JobDispatcher as njq

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

	db.delete_db_session()

