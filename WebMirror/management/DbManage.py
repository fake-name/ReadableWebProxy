
import time
import datetime
import re
import os
import os.path
import tqdm
import traceback
from concurrent.futures import ThreadPoolExecutor

import urllib.error
import urllib.parse

from sqlalchemy import and_
from sqlalchemy import or_
import sqlalchemy.exc

if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()

import common.database as db


import flags
import pprint
import config

import WebMirror.UrlUpserter
import WebMirror.OutputFilters.rss.FeedDataParser
import WebMirror.OutputFilters.util.feedNameLut
import common.rss_func_db as rfdb
import astor
import astor.source_repr

import WebMirror.API


def exposed_reset_in_progress():
	'''
	Reset all rows that are in the fetching process to new.
	'''

	WebMirror.UrlUpserter.resetInProgress()


def exposed_disable_available():
	'''
	Set all rows in the 'new', 'fetching', 'processing', or 'specialty_deferred' state to the 'manually_deferred' state
	'''


	commit_interval =   50000
	step            =  150000
	commit_every    =      30
	last_commit     = time.time()

	with db.session_context(override_timeout_ms=60 * 1000 * 15) as sess:
		try:
			# sess.execute('''SET enable_bitmapscan TO off;''')
			print("Disabling available links!")
			print("Getting minimum row in need or update..")
			start = sess.execute("""SELECT min(id),  max(id) FROM web_pages WHERE (state = 'new' OR state = 'fetching' OR state = 'processing' OR state = 'specialty_deferred')""")
			# start = sess.execute("""SELECT min(id) FROM web_pages WHERE (state = 'fetching' OR state = 'processing' OR state = 'specialty_deferred') OR state = 'specialty_deferred' OR state = 'specialty_ready'""")
			start, stop = list(start)[0]
			if start is None:
				print("No rows to reset!")
				return
			print("Minimum row ID: ", start, "Maximum row ID: ", stop)


			print("Need to fix rows from %s to %s" % (start, stop))
			start = start - (start % step)

			changed = 0
			tot_changed = 0
			# for idx in range(start, stop, step):
			for idx in tqdm.tqdm(range(start, stop, step), desc="Manually Deferring all URLs"):
				try:
					# SQL String munging! I'm a bad person!
					# Only done because I can't easily find how to make sqlalchemy
					# bind parameters ignore the postgres specific cast
					# The id range forces the query planner to use a much smarter approach which is much more performant for small numbers of updates
					have = sess.execute("""UPDATE
												web_pages
											SET
												state = 'manually_deferred'
											WHERE
												(state = 'new' OR state = 'fetching' OR state = 'processing' OR state = 'specialty_deferred')
											AND
												id > {}
											AND
												id <= {}
												;""".format(idx, idx+step))

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
						last_commit     = time.time()

					if time.time() > last_commit + commit_every:
						last_commit     = time.time()
						print("Committing (%s changed rows, timed out)...." % changed, end=' ')
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

def exposed_manually_defer_all():
	'''
	Set all rows in the 'new', 'fetching', 'processing', or 'specialty_deferred' state to the 'single_step_deferred' state
	'''


	commit_interval =   50000
	step            =  150000
	commit_every    =      30
	last_commit     = time.time()

	with db.session_context(override_timeout_ms=60 * 1000 * 15) as sess:
		try:
			# sess.execute('''SET enable_bitmapscan TO off;''')
			print("Disabling available links!")
			print("Getting minimum row in need or update..")
			start = sess.execute("""SELECT min(id),  max(id) FROM web_pages WHERE (state = 'new' OR state = 'fetching' OR state = 'processing' OR state = 'specialty_deferred')""")
			# start = sess.execute("""SELECT min(id) FROM web_pages WHERE (state = 'fetching' OR state = 'processing' OR state = 'specialty_deferred') OR state = 'specialty_deferred' OR state = 'specialty_ready'""")
			start, stop = list(start)[0]
			if start is None:
				print("No rows to reset!")
				return
			print("Minimum row ID: ", start, "Maximum row ID: ", stop)


			print("Need to fix rows from %s to %s" % (start, stop))
			start = start - (start % step)

			changed = 0
			tot_changed = 0
			# for idx in range(start, stop, step):
			for idx in tqdm.tqdm(range(start, stop, step), desc="Manually Deferring all URLs"):
				try:
					# SQL String munging! I'm a bad person!
					# Only done because I can't easily find how to make sqlalchemy
					# bind parameters ignore the postgres specific cast
					# The id range forces the query planner to use a much smarter approach which is much more performant for small numbers of updates
					have = sess.execute("""UPDATE
												web_pages
											SET
												state = 'single_step_deferred'
											WHERE
												(state = 'new' OR state = 'fetching' OR state = 'processing' OR state = 'specialty_deferred' OR state = 'complete')
											AND
												id > {}
											AND
												id <= {}
												;""".format(idx, idx+step))

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
						last_commit     = time.time()

					if time.time() > last_commit + commit_every:
						last_commit     = time.time()
						print("Committing (%s changed rows, timed out)...." % changed, end=' ')
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

def exposed_enable_manually_deferred():
	'''
	Set all rows in the 'manually_deferred' state to the 'new' state
	'''


	commit_interval =   50000
	step            =  150000
	commit_every    =      30
	last_commit     = time.time()

	with db.session_context(override_timeout_ms=60 * 1000 * 15) as sess:
		try:
			# sess.execute('''SET enable_bitmapscan TO off;''')
			print("Enabling Manually Deferred!")
			print("Getting minimum row in need or update..")
			start = sess.execute("""SELECT min(id),  max(id) FROM web_pages WHERE (state = 'manually_deferred')""")
			# start = sess.execute("""SELECT min(id) FROM web_pages WHERE (state = 'fetching' OR state = 'processing' OR state = 'specialty_deferred') OR state = 'specialty_deferred' OR state = 'specialty_ready'""")
			start, stop = list(start)[0]
			if start is None:
				print("No rows to reset!")
				return
			print("Minimum row ID: ", start, "Maximum row ID: ", stop)


			print("Need to fix rows from %s to %s" % (start, stop))
			start = start - (start % step)

			changed = 0
			tot_changed = 0
			# for idx in range(start, stop, step):
			for idx in tqdm.tqdm(range(start, stop, step), desc="Enabling Manually Deferred!"):
				try:
					# SQL String munging! I'm a bad person!
					# Only done because I can't easily find how to make sqlalchemy
					# bind parameters ignore the postgres specific cast
					# The id range forces the query planner to use a much smarter approach which is much more performant for small numbers of updates
					have = sess.execute("""UPDATE
												web_pages
											SET
												state = 'new'
											WHERE
												(state = 'manually_deferred')
											AND
												id > {}
											AND
												id <= {}
												;""".format(idx, idx+step))

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
						last_commit     = time.time()

					if time.time() > last_commit + commit_every:
						last_commit     = time.time()
						print("Committing (%s changed rows, timed out)...." % changed, end=' ')
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



def exposed_reset_walk_epochs():
	'''
	Set the walk epoch for all rows in the table to zero

	Useful when the walk interval has been changed to a larger value, as this can cause the
	next rewalk to be pushed far out into the future and block re-fetching for far longer then intended

	'''

	commit_interval =   10000
	step            =   50000
	commit_every    =      30
	last_commit     = time.time()

	with db.session_context(override_timeout_ms=60 * 1000 * 15) as sess:
		try:
			# sess.execute('''SET enable_bitmapscan TO off;''')
			print("Getting minimum row in need or update..")
			start = sess.execute("""SELECT min(id),  max(id) FROM web_pages WHERE epoch <> 0""")
			# start = sess.execute("""SELECT min(id) FROM web_pages WHERE (state = 'fetching' OR state = 'processing') OR state = 'specialty_deferred' OR state = 'specialty_ready'""")
			start, stop = list(start)[0]
			if start is None:
				print("No rows to reset!")
				return
			print("Minimum row ID: ", start, "Maximum row ID: ", stop)


			print("Need to fix rows from %s to %s" % (start, stop))
			start = start - (start % step)

			changed = 0
			tot_changed = 0
			# for idx in range(start, stop, step):
			for idx in tqdm.tqdm(range(start, stop, step), desc="Resetting Epochs"):
				try:
					# SQL String munging! I'm a bad person!
					# Only done because I can't easily find how to make sqlalchemy
					# bind parameters ignore the postgres specific cast
					# The id range forces the query planner to use a much smarter approach which is much more performant for small numbers of updates
					have = sess.execute("""UPDATE
												web_pages
											SET
												epoch = 0
											WHERE
												epoch <> 0
											AND
												id > {}
											AND
												id <= {}
												;""".format(idx, idx+step))

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
						last_commit     = time.time()

					if time.time() > last_commit + commit_every:
						last_commit     = time.time()
						print("Committing (%s changed rows, timed out)...." % changed, end=' ')
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

