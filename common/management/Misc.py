
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
import WebMirror.NewJobQueue

import RawArchiver.RawActiveModules
import RawArchiver.RawEngine

import common.database as db
import common.Exceptions
import common.management.file_cleanup

import Misc.HistoryAggregator.Flatten

import flags
import config
from config import C_RAW_RESOURCE_DIR

import WebMirror.TimedTriggers.QueueTriggers
import pickle
import pprint

def exposed_print_scheduled_jobs():
	'''

	'''
	sess = db.get_db_session()

	items = sess.execute("""
		SELECT
			id, next_run_time , job_state
		FROM
			apscheduler_jobs
	""")
	items = list(items)
	for tid, nextcall, content in items:
		print("Job: ", tid.ljust(30), str(nextcall).rjust(20))

		dat = pickle.loads(content)
		pprint.pprint(dat)
