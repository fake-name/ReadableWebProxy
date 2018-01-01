
import os
import os.path
import shutil
from tqdm import tqdm

if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()


import RawArchiver.RawActiveModules
import RawArchiver.RawEngine

import common.database as db
import common.Exceptions
import common.management.file_cleanup

from config import C_RAW_RESOURCE_DIR
from sqlalchemy_continuum.utils import version_table



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
	with tqdm(total=res) as pbar:
		bad = 0
		for row in sess1.query(db.RawWebPages).yield_per(1000):
			if not any([mod.cares_about_url(row.url) for mod in RawArchiver.RawActiveModules.ACTIVE_MODULES]):
				last_bad = row.netloc
				# print("Unwanted: ", row.url)
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

	ctbl = version_table(db.RawWebPages)

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
	with tqdm(total=res) as pbar:
		bad = 0

		for rurl, rnetloc in sess1.query(ctbl.c.url, ctbl.c.netloc).yield_per(1000):
			if not any([mod.cares_about_url(rurl) for mod in RawArchiver.RawActiveModules.ACTIVE_MODULES]):
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
