

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

	sess = common.database.get_db_session()
	sess.query(common.database.RawWebPages) \
		.filter(
				(common.database.RawWebPages.state == "fetching")           |
				(common.database.RawWebPages.state == "processing")
				)   \
		.update({common.database.RawWebPages.state : "new"})
	sess.commit()
	sess.close()
	common.database.delete_db_session()


