
import logging
import datetime
import random
import WebMirror.database as db
import multiprocessing
import time
random.seed()
# import WebMirror.rules
# import WebMirror.LogBase as LogBase
# import runStatus
# import time
# import os.path
# import os
# import sys
# import sqlalchemy.exc

# from sqlalchemy import desc

# from sqlalchemy.sql import text
# from sqlalchemy import distinct
# from sqlalchemy.dialects import postgresql

# import WebMirror.util.urlFuncs
# import urllib.parse
# import traceback
# import datetime

# from sqlalchemy.sql import text
# from sqlalchemy.sql import func
# import WebMirror.util.webFunctions as webFunctions

# import hashlib
# from WebMirror.Fetch import DownloadException
# import WebMirror.Fetch
# import WebMirror.database as db
# from config import C_RESOURCE_DIR

# from activePlugins import INIT_CALLS

# if "debug" in sys.argv:
# 	CACHE_DURATION = 1
# 	RSC_CACHE_DURATION = 1
# 	# CACHE_DURATION = 60 * 5
# 	# RSC_CACHE_DURATION = 60 * 60 * 5
# else:
# 	CACHE_DURATION = 60 * 60 * 24 * 7
# 	RSC_CACHE_DURATION = 60 * 60 * 24 * 147

ACTIVE_FETCHES = {
	# Populated at runtime
}

FETCH_LOCK = multiprocessing.Lock()

log = logging.getLogger("Main.Web.SpecialCaseHandler")

def handleRemoteFetch(params, job, engine):
	# print("Remote fetch command!")
	pass

def handleRateLimiting(params, job, engine):
	allowable = params[0]
	with FETCH_LOCK:
		if not job.netloc in ACTIVE_FETCHES:
			ACTIVE_FETCHES[job.netloc] = 0

	log.info("Active fetchers for domain %s - %s", job.netloc, ACTIVE_FETCHES[job.netloc])
	if ACTIVE_FETCHES[job.netloc] > allowable:
		log.info("Too many instances of fetchers for domain %s active. Forcing requests to sleep for a while", job.netloc)
		job.ignoreuntiltime = datetime.datetime.now() + datetime.timedelta(seconds=60*5 + random.randrange(0, 60*5))
		db.get_session().commit()
		return
	else:
		with FETCH_LOCK:
			ACTIVE_FETCHES[job.netloc] += 1
		engine.do_job(job)
		time.sleep(5)
		with FETCH_LOCK:
			ACTIVE_FETCHES[job.netloc] -= 1



dispatchers = {
	'remote_fetch' : handleRemoteFetch,
	'rate_limit'   : handleRateLimiting,

}


def handleSpecialCase(job, engine, rules):
	commands = rules[job.netloc]
	op, params = commands[0], commands[1:]
	if op in dispatchers:
		dispatchers[op](params, job, engine)
	else:
		log.error("Error! Unknown special-case filter!")
		print("Filter name: '%s', parameters: '%s', job URL: '%s'", op, params, job.url)
