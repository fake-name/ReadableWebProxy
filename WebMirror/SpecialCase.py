
if __name__ == '__main__':
	import logSetup
	logSetup.initLogging()

import logging
import datetime
import random
import multiprocessing
import traceback
import time
import queue
import urllib.parse

from sqlalchemy import desc
import common.database as db


import WebMirror.JobUtils

random.seed()

ACTIVE_FETCHES = {
	# Populated at runtime
}

FETCH_LOCK       = multiprocessing.Lock()
RATE_LIMIT_ITEMS = {}


log = logging.getLogger("Main.Web.SpecialCaseHandler")

class SpecialCaseFilterMissing(RuntimeError):
	pass

def handleRateLimiting(params, rid, joburl, netloc, job_aggregator_instance):
	log.info("Special case handler pushing item for url %s into delay queue!", joburl)
	with FETCH_LOCK:
		if not netloc in RATE_LIMIT_ITEMS:
			q = multiprocessing.Queue()
			q.put((rid, joburl, netloc))
			item = {
				'ntime' : time.time(),
				"queue" : q
			}
			RATE_LIMIT_ITEMS[netloc] = item
		else:
			if RATE_LIMIT_ITEMS[netloc]['ntime'] == -1:
				RATE_LIMIT_ITEMS[netloc]['ntime'] = time.time()
			RATE_LIMIT_ITEMS[netloc]['queue'].put((rid, joburl, netloc))


def handleRemoteRenderFetch(params, rid, joburl, netloc, job_aggregator_instance):
	print('handleRemoteRenderFetch', params, rid, joburl, netloc)

	raw_job = WebMirror.JobUtils.buildjob(
		module         = 'WebRequest',
		call           = 'chromiumGetRenderedItem',
		dispatchKey    = "fetcher",
		jobid          = rid,
		args           = [joburl],
		kwargs         = {},
		additionalData = {'mode' : 'fetch'},
		postDelay      = 0,
		serialize      = True,
	)

	job_aggregator_instance.put_job(raw_job)

def handleRemoteChromeFetch(params, rid, joburl, netloc, job_aggregator_instance):
	print('handleRemoteRenderFetch', params, rid, joburl, netloc)

	raw_job = WebMirror.JobUtils.buildjob(
		module         = 'WebRequest',
		call           = 'chromiumGetRenderedItem',
		dispatchKey    = "fetcher",
		jobid          = rid,
		args           = [joburl],
		kwargs         = {},
		additionalData = {'mode' : 'fetch'},
		postDelay      = 0,
		serialize      = True,
	)

	job_aggregator_instance.put_job(raw_job)

def qidianSmartFeedFetch(params, rid, joburl, netloc, job_aggregator_instance):
	print('qidianSmartFeedFetch', params, rid, joburl, netloc)


	sess = db.get_db_session(flask_sess_if_possible=False)
	have = sess.query(db.QidianFeedPostMeta).order_by(desc(db.QidianFeedPostMeta.id)).limit(500).all()

	meta_dict = {}
	for row in have:
		meta_dict[row.contentid] = row.meta

	sess.commit()


	raw_job = WebMirror.JobUtils.buildjob(
		module         = 'PreprocessFetch',
		call           = 'qidianSmartFeedFetch',
		dispatchKey    = "fetcher",
		jobid          = rid,
		args           = [joburl],
		kwargs         = {'meta' : meta_dict},
		additionalData = {},
		postDelay      = 0,
		serialize      = "QidianModule",
	)

	# print("Raw job:")
	# print(raw_job)
	# return raw_job

	job_aggregator_instance.put_job(raw_job)

def localContentFetch(params, rid, joburl, netloc, job_aggregator_instance):
	log.info("Special case handler for locally fetched content: %s!", joburl)
	job_aggregator_instance.blocking_put_response(
		{
			'mode' : 'local_fetch',
			'joburl' : joburl,
			'jobid' : rid
		}
	)

dispatchers = {
	'rate_limit'            : handleRateLimiting,
	'chrome_render_fetch'   : handleRemoteRenderFetch,
	'qudian_feed_forward'   : qidianSmartFeedFetch,
	'local_fetch'           : localContentFetch,
}


def getSpecialCase(specialcase):
	log.info("Special case handler checking for deferred fetches.")
	with FETCH_LOCK:
		# print()
		# print("RATE_LIMIT_ITEMS")
		# for key, value in RATE_LIMIT_ITEMS.items():
		# 	print("	%s -> %s (%s)" % (key, value['queue'].qsize(), value))
		# print()
		for key in RATE_LIMIT_ITEMS.keys():
			if RATE_LIMIT_ITEMS[key]['ntime'] < time.time():
				try:
					rid, joburl, netloc = RATE_LIMIT_ITEMS[key]['queue'].get_nowait()

					rate = specialcase[netloc][1]

					RATE_LIMIT_ITEMS[key]['ntime'] += rate
					log.info("Deferred special case item for url '%s' ready. Returning.", joburl)
					return rid, joburl, netloc
				except queue.Empty:
					RATE_LIMIT_ITEMS[key]['ntime'] = -1
			else:
				log.info("Not yet ready to fetch for '%s' (%s < %s)", key, RATE_LIMIT_ITEMS[key]['ntime'], time.time())

	return None, None, None


def pushSpecialCase(specialcase, rid, joburl, netloc, job_aggregator_instance):
	'''
	Handle processing AMQP queue responses here.
	Return true if there was a queue responseto handle, false if there was not.
	'''

	if netloc in specialcase:
		commands = specialcase[netloc]
	else:
		matching_keys = [joburl for tmp in specialcase.keys() if joburl in tmp]
		if matching_keys:
			if not all([specialcase[matching_keys[0]] == specialcase[match_key] for match_key in matching_keys]):
				errstr = "Multiple keys can only match if all the special_case handlers for the keys are the same: %s, %s (%s)" % (
					matching_keys,
					[specialcase[match_key] for match_key in matching_keys if match_key in specialcase],
					(rid, joburl, netloc))
				assert True, errstr
			commands = specialcase[matching_keys[0]]
		else:
			raise ValueError("SpecialCase handler called for URL (%s, %s) without handler!" % (joburl, netloc))


	op, params = commands[0], commands[1:]

	if op in dispatchers:
		return dispatchers[op](
			params                  = params,
			rid                     = rid,
			joburl                  = joburl,
			netloc                  = netloc,
			job_aggregator_instance = job_aggregator_instance)
	else:
		log.error("Error! Unknown special-case filter!")
		log.error("Filter name: '%s', parameters: '%s', job conf: '%s'", op, params, (rid, joburl, netloc))
		err_msg = "Unknown special-case filter! Filter name: '%s', parameters: '%s', job conf: '%s'", op, params, (rid, joburl, netloc)
		raise SpecialCaseFilterMissing(err_msg)


def getSpecialCaseHandler(specialcase, joburl=None, netloc=None):
	if not (netloc or joburl):
		raise RuntimeError("You need to pass either joburl or netloc!")

	if not netloc:   # We assume joburl must be defined if netloc is not, at this point
		netloc = urllib.parse.urlsplit(joburl).netloc

	if netloc in specialcase:
		# No special case for netloc
		return specialcase[netloc]

	if joburl in specialcase:
		return specialcase[joburl]

	return None

def haveSpecialCase(specialcase, joburl, netloc):

	# Short circuit for the homepage root, so it
	# always gets fetched immediately.
	if joburl == "http://www.novelupdates.com/" or joburl == "http://www.novelupdates.com":
		return False

	if netloc in specialcase:
		return True

	if joburl in specialcase:
		return True


	return False

def test():
	pass

if __name__ == '__main__':
	test()



