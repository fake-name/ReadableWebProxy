
import calendar
import datetime
import json
import os
import os.path
import shutil
import traceback
from concurrent.futures import ThreadPoolExecutor

import urllib.error
import urllib.parse

from sqlalchemy import and_
from sqlalchemy import or_
from sqlalchemy_continuum.utils import version_table

if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()

from WebMirror.Engine import SiteArchiver
import WebMirror.OutputFilters.util.feedNameLut as feedNameLut
import WebMirror.rules
import WebMirror.SiteSync.fetch
import WebMirror.SpecialCase

import RawArchiver.RawActiveModules
import RawArchiver.RawEngine

import common.database as db
import common.Exceptions
import common.management.file_cleanup

import flags
import config
from config import C_RAW_RESOURCE_DIR



def exposed_purge_raw_invalid_urls():
	'''
	Delete all raw-archiver rows that aren't
	attached to a archiver module.
	'''

	sess = db.get_db_session()

	bad = 0
	for row in sess.query(db.RawWebPages).yield_per(1000).all():
		if not any([mod.cares_about_url(row.url) for mod in RawArchiver.RawActiveModules.ACTIVE_MODULES]):
			print("Unwanted: ", row.url)
			sess.delete(row)
			bad += 1
		if bad > 5000:
			print("Committing!")
			bad = 0
			sess.commit()
	sess.commit()


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
	for row in sess.query(db.RawWebPages).yield_per(1000).all():
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
	'''
	common.management.file_cleanup.sync_raw_with_filesystem()

def exposed_delete_unattached_filtered_files():
	'''
	Basically another version of delete_unattached_raw_files
	I don't remember why there are two versions.

	'''
	common.management.file_cleanup.sync_filtered_with_filesystem()


