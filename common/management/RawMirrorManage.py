
import os
import os.path
import shutil
import time
import tqdm
import sqlalchemy.exc

import RawArchiver.RawActiveModules
import RawArchiver.RawEngine

import common.database as db
import common.Exceptions
import common.management.file_cleanup
import common.global_constants
import common.util.urlFuncs as urlFuncs

from config import C_RAW_RESOURCE_DIR
from sqlalchemy_continuum_vendored.utils import version_table


def exposed_purge_raw_invalid_urls():
	'''
	Delete all raw-archiver rows that aren't
	attached to a archiver module.
	'''

	sess1 = db.get_db_session(postfix='iter_sess')
	sess2 = db.get_db_session(postfix='delete_sess')

	print("Loading files from database...")
	# spinner1 = Spinner()

	est = sess1.execute("SELECT reltuples::BIGINT AS estimate FROM pg_class WHERE relname='raw_web_pages';")
	res = est.scalar()
	print("Estimated row-count: %s" % res)

	last_bad = ""
	last_commit = 0
	deleted = 0
	maxlen = 0
	changed_rows = 0
	total_rows = 0
	with tqdm.tqdm(total=res) as pbar:
		bad = 0
		for row in sess1.query(db.RawWebPages).yield_per(1000):
			modules_wants_url = any([mod.cares_about_url(row.url) for mod in RawArchiver.RawActiveModules.ACTIVE_MODULES])
			has_badwords      = any([badword in row.url for badword in common.global_constants.GLOBAL_BAD_URLS])
			if not modules_wants_url or has_badwords:
				last_bad = row.netloc
				print("Unwanted: ", row.url)
				# sess1.delete(row)

				changed_rows = sess2.query(db.RawWebPages) \
					.filter(db.RawWebPages.url == row.url) \
					.delete(synchronize_session=False)

				bad += 1
				deleted += 1

			total_rows += 1
			if bad > 5000:
				# print("Committing!")
				bad = 0
				last_commit = deleted
				sess2.commit()
			else:
				msg = "Deleted: %s, since commit: %s, last_bad: '%s' (%s, %s%%)" % \
					(deleted, deleted-last_commit, last_bad, changed_rows, 100.0*(deleted / total_rows))

				maxlen = max(len(msg), maxlen)
				pbar.set_description(msg.ljust(maxlen), refresh=False)
			pbar.update(n=1)

	sess1.commit()
	sess2.commit()

def exposed_purge_raw_invalid_urls_from_history():
	'''
	Delete all raw-archiver rows that aren't
	attached to a archiver module.
	'''

	sess1 = db.get_db_session(postfix='iter_sess')
	sess2 = db.get_db_session(postfix='delete_sess')

	ctbl = version_table(db.RawWebPages.__table__)

	print("Loading files from database...")
	# spinner1 = Spinner()

	est = sess1.execute("SELECT reltuples::BIGINT AS estimate FROM pg_class WHERE relname='raw_web_pages_version';")
	res = est.scalar()
	print("Estimated row-count: %s" % res)

	last_bad = ""
	deleted = 0
	total_rows = 0
	last_commit = 0
	maxlen = 0
	changed_rows = 0
	with tqdm.tqdm(total=res) as pbar:
		bad = 0

		for rurl, rnetloc in sess1.query(ctbl.c.url, ctbl.c.netloc).yield_per(1000):
			modules_wants_url = any([mod.cares_about_url(rurl) for mod in RawArchiver.RawActiveModules.ACTIVE_MODULES])
			has_badwords      = any([badword in rurl for badword in common.global_constants.GLOBAL_BAD_URLS])
			if not modules_wants_url or has_badwords:
				last_bad = rnetloc
				# print("Unwanted: ", rurl)

				changed_rows = sess2.query(ctbl) \
					.filter(ctbl.c.url == rurl) \
					.delete(synchronize_session=False)

				bad += 1
				deleted += 1
			total_rows += 1

			if bad > 5000:
				# print("Committing!")
				bad = 0
				last_commit = deleted
				sess2.commit()
				# pbar.set_description("Doing Commit", refresh=True)
			else:
				msg = "Deleted: %s, since commit: %s, last_bad: '%s' (%s, %s%%)" % \
					(deleted, deleted-last_commit, last_bad, changed_rows, 100.0*(deleted / total_rows))
				maxlen = max(len(msg), maxlen)
				pbar.set_description(msg.ljust(maxlen), refresh=False)


			pbar.update(n=1)

	sess1.commit()
	sess2.commit()


def to_locpath(fqpath):
	assert fqpath.startswith(C_RAW_RESOURCE_DIR)

	locpath = fqpath[len(C_RAW_RESOURCE_DIR):]
	if locpath.startswith("/"):
		locpath = locpath[1:]
	return locpath

def exposed_reset_raw_in_progress():
	'''
	Reset raw downloads that are in progress.
	'''
	RawArchiver.RawUrlUpserter.resetRawInProgress()





def set_new_to_skipped():
	print("Resetting any stalled downloads from the previous session.")


	commit_interval =  50000
	step            =  50000
	commit_every    =  30
	last_commit     = time.time()

	with db.session_context(override_timeout_ms=60 * 1000 * 15) as sess:
		try:
			# sess.execute('''SET enable_bitmapscan TO off;''')
			print("Getting minimum row in need or update..")
			start = sess.execute("""SELECT min(id) FROM raw_web_pages WHERE state = 'fetching' OR state = 'processing' OR state = 'new'""")
			# start = sess.execute("""SELECT min(id) FROM raw_web_pages WHERE state = 'fetching' OR state = 'processing' OR state = 'new' OR state = 'specialty_deferred' OR state = 'specialty_ready'""")
			start = list(start)[0][0]
			if start is None:
				print("No rows to reset!")
				return
			print("Minimum row ID:", start, "getting maximum row...")
			stop = sess.execute("""SELECT max(id) FROM raw_web_pages WHERE state = 'fetching' OR state = 'processing' OR state = 'new'""")
			# stop = sess.execute("""SELECT max(id) FROM raw_web_pages WHERE state = 'fetching' OR state = 'processing' OR state = 'new' OR state = 'specialty_deferred' OR state = 'specialty_ready'""")
			stop = list(stop)[0][0]
			print("Maximum row ID: ", stop)


			print("Need to fix rows from %s to %s" % (start, stop))
			start = start - (start % step)

			changed = 0
			tot_changed = 0
			# for idx in range(start, stop, step):
			for idx in tqdm.tqdm(range(start, stop, step), desc="Resetting raw URLs"):
				try:
					# SQL String munging! I'm a bad person!
					# Only done because I can't easily find how to make sqlalchemy
					# bind parameters ignore the postgres specific cast
					# The id range forces the query planner to use a much smarter approach which is much more performant for small numbers of updates
					have = sess.execute("""UPDATE
												raw_web_pages
											SET
												state = 'skipped'
											WHERE
												(state = 'fetching' OR state = 'processing' OR state = 'new')
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



def reset_root_skipped_to_new():
	print("Initializing all start URLs in the database")
	with common.database.session_context() as sess:
		for module in RawArchiver.RawActiveModules.ACTIVE_MODULES:
			for starturl in module.get_start_urls():
				have = sess.query(common.database.RawWebPages) \
					.filter(common.database.RawWebPages.url == starturl)   \
					.count()
				if have:
					if have.state == 'skipped':
						have.state = 'new'
				else:
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




def exposed_reset_raw_incremental_fetch():
	'''
	Reset the raw fetch incremental fetch.
	'''
	set_new_to_skipped()
	reset_root_skipped_to_new()



def exposed_reset_raw_missing():
	'''
	Retrigger all raw-archive links that don't seem to have
	a corresponding file on-disk.
	'''

	sess = db.get_db_session()

	bad = 0
	for row in sess.query(db.RawWebPages).yield_per(1000):
		if row.fspath:


			nl, rest = row.fspath.split("/", 1)
			nl = nl.split(".")
			nl.reverse()
			nl = "/".join(nl)
			newp = nl + "/" + rest

			old = os.path.join(C_RAW_RESOURCE_DIR, "old", row.fspath)
			new = os.path.join(C_RAW_RESOURCE_DIR, newp)

			if os.path.exists(new) and row.fspath == newp:
				#print("Nothing to do: ", row.fspath, new, newp)
				pass
			elif os.path.exists(new):
				print("Relinking: ", newp, row.fspath)
				row.fspath = to_locpath(new)
				bad += 1
			elif os.path.exists(old):
				dirPath = os.path.split(new)[0]
				if not os.path.exists(dirPath):
					os.makedirs(dirPath)
				shutil.move(old, new)

				row.fspath = to_locpath(new)
				bad += 1
				print("Moving: ", old, new)
			else:
				row.state = "new"
				bad += 1
		else:
			row.state = "new"
			bad += 1

		if bad > 25000:
			print("Committing!")
			bad = 0
			sess.commit()
	sess.commit()


def exposed_delete_unattached_raw_files():
	'''
	Load the local content files from the raw archiver, and compare them
	against the database. Extra files that are not in the database will then
	be deleted.
	This also resets the dlstate of for addresses where the file is missing.
	'''
	common.management.file_cleanup.sync_raw_with_filesystem()




def exposed_drop_raw_priorities():
	'''
	Reset the priority of every row in the table to the IDLE_PRIORITY level
	'''

	# We have a maximum commit interval so we don't hold a transaction open for extremely long periods of time,
	# as doing so can cause other portions of the system to time out.
	commit_interval_s  = 30
	step               = 10000

	with db.session_context(override_timeout_ms=30*60*1000) as sess:
		print("Getting minimum row in need or update..")
		start = sess.execute("""SELECT min(id) FROM raw_web_pages WHERE priority != 9""")
		start = list(start)[0][0]
		if start is None:
			print("No rows to reset!")
			return
		print("Minimum row ID: ", start, "getting maximum row...")
		stop = sess.execute("""SELECT max(id) FROM raw_web_pages WHERE priority != 9""")
		stop = list(stop)[0][0]
		print("Maximum row ID: ", stop)

		if not start:
			print("No null rows to fix!")
			return

		print("Need to fix rows from %s to %s" % (start, stop))
		start = start - (start % step)

		changed = 0
		changed_tot = 0
		last_commit = time.time()
		pb = tqdm.tqdm(range(start, stop, step), desc='Dropping raw priorities.')
		for idx in pb:
			try:
				# SQL String munging! I'm a bad person!
				# Only done because I can't easily find how to make sqlalchemy
				# bind parameters ignore the postgres specific cast
				# The id range forces the query planner to use a much smarter approach which is much more performant for small numbers of updates
				have = sess.execute("""update raw_web_pages set priority = 9 where priority != 9 AND id > {} AND id <= {};""".format(idx, idx+step))
				# print()

				# processed  = idx - start
				# total_todo = stop - start
				desc = '(drop_priorities) -> %6i, %6i, %6i' % (have.rowcount, changed, changed_tot)
				pb.set_description(desc)

				# print('\r%10i, %10i, %7.4f, %6i, %6i, %6i\r' % (idx, stop, processed/total_todo * 100, have.rowcount, changed, changed_tot), end="", flush=True)
				changed += have.rowcount
				changed_tot += have.rowcount
				if changed > step * 10 or (time.time() - last_commit) > commit_interval_s:
					print("Committing (%s changed rows)...." % changed, end=' ')
					sess.commit()
					print("done")
					changed = 0
					last_commit = time.time()

			except sqlalchemy.exc.OperationalError:
				sess.rollback()
			except sqlalchemy.exc.InvalidRequestError:
				sess.rollback()


		sess.commit()
