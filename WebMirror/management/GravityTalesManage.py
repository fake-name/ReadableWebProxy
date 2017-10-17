
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
import sqlalchemy.exc
from sqlalchemy_continuum.utils import version_table

if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()

import common.database as db
import common.Exceptions
import common.management.file_cleanup

import Misc.HistoryAggregator.Consolidate

import flags
import pprint
import config
from config import C_RAW_RESOURCE_DIR

import WebMirror.OutputFilters.rss.FeedDataParser


def exposed_delete_gravitytales_bot_blocked_pages():
	'''
	Delete the "checking you're not a bot" garbage pages
	that sometimes get through the gravitytales scraper.
	'''
	sess = db.get_db_session()
	tables = [
		db.WebPages.__table__,
		version_table(db.WebPages)
	]

	for ctbl in tables:
		update = ctbl.delete() \
			.where(ctbl.c.netloc == "gravitytales.com") \
			.where(ctbl.c.content.like('%<div id="bot-alert" class="alert alert-info">%'))
		print(update)
		sess.execute(update)
		sess.commit()
