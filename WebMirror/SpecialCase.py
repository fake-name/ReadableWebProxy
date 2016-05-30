
if __name__ == '__main__':
	import logSetup
	logSetup.initLogging()

import logging
import datetime
import random
import WebMirror.database as db
import multiprocessing
import traceback
import time

from WebMirror.SpecialHandlers import AmqpHandler

random.seed()

ACTIVE_FETCHES = {
	# Populated at runtime
}

FETCH_LOCK = multiprocessing.Lock()

log = logging.getLogger("Main.Web.SpecialCaseHandler")


AMQP_FETCHER = None
def startAmqpFetcher():
	global AMQP_FETCHER
	if AMQP_FETCHER != None:
		log.error("AmqpFetcher RPC instantiated twice!")
		for line in traceback.format_exc().split("\n"):
			log.error(line)

		raise RuntimeError("AmqpFetcher instantiated twice!")

	AMQP_FETCHER = AmqpHandler.AmqpRemoteJobManager()

def stopAmqpFetcher():
	global AMQP_FETCHER
	print("Trying to stop fetcher")
	if AMQP_FETCHER == None:
		log.error("Cannot stop AMQP fetcher that is not running!!")
		try:
			fexc = traceback.format_exc()
		except Exception:
			return

		for line in fexc.split("\n"):
			log.error(line)

		raise RuntimeError("Cannot stop AMQP fetcher that is not running!!")

	AMQP_FETCHER.close()
	del AMQP_FETCHER
	AMQP_FETCHER = None



def dispatchRemoteFetch(params, job):
	if AMQP_FETCHER == None:
		return

	print("Remote fetch command!")
	module, call = params

	assert job.id != None

	# Be sure to update the DB state.
	job.state = 'specialty_deferred'
	db.get_db_session().commit()

	raw_job = AmqpHandler.buildjob(
			module         = module,
			call           = call,
			dispatchKey    = "fetcher",
			jobid          = job.id,
			args           = [job.url],
			kwargs         = {},
			additionalData = {'mode' : 'fetch'},
			postDelay      = 5
		)


	AMQP_FETCHER.put_job(raw_job)

def handleRemoteFetch(params, job, engine, db_sess):

	dispatchRemoteFetch(params, job)
	for x in range(60*5):
		time.sleep(1)
		# Clear the implicit transaction context so we can actually see changes by other threads.
		db_sess.rollback()
		db_sess.refresh(job)

		print("Sleeping. Job state = ", job.state)
		if job.state == "specialty_ready":
			return job
	return None

def doRemoteHead(url, referrer):
	# remote_fetch, WebRequest, getItem
	raw_job = AmqpHandler.buildjob(
			module         = 'NUWebRequest',
			call           = 'getHead',
			dispatchKey    = "fetcher",
			jobid          = url,
			args           = [url],
			kwargs         = {'addlHeaders' : {'Referer' : referrer}},
			additionalData = {
					'mode' : 'head',
					'wrapped_url' : url,
					'referrer' : referrer,
				},
			postDelay      = 0
		)

	# print(raw_job)
	AMQP_FETCHER.put_job(raw_job)


def blockingRemoteHead(url, referrer):

	retries = 2 # 60 seconds.
	timeout = 60*5 # 60 seconds.
	db_sess = db.get_db_session()

	transmitted = False
	for y in range(retries):
		for x in range(timeout):
			row =  db_sess.query(db.NuOutboundWrapperMap)                    \
				.filter(db.NuOutboundWrapperMap.container_page == referrer ) \
				.filter(db.NuOutboundWrapperMap.link_url       == url )      \
				.scalar()
			if row:
				print("Had outbound row wrapper for %s" % url)
				return row.target_url
			if not transmitted:
				transmitted = True
				doRemoteHead(url, referrer)
			time.sleep(1)
			db_sess.rollback()

			# TODO: EXIT FLAG CHECKING GOES HERE

			print("[blockingRemoteHead()] sleeping %s!" % (timeout-x))
	raise RuntimeError("Failed to fetch response for remote HEAD call!")


def handleSoRemoteFetch(params, job, engine, db_sess):
	print("StoriesOnline Remote fetch command!")
	pass

def handleRateLimiting(params, job, engine, db_sess):
	allowable = params[0]
	with FETCH_LOCK:
		if not job.netloc in ACTIVE_FETCHES:
			ACTIVE_FETCHES[job.netloc] = 0

	log.info("Active fetchers for domain %s - %s", job.netloc, ACTIVE_FETCHES[job.netloc])
	if ACTIVE_FETCHES[job.netloc] > allowable:
		log.info("Too many instances of fetchers for domain %s active. Forcing requests to sleep for a while", job.netloc)
		job.ignoreuntiltime = datetime.datetime.now() + datetime.timedelta(seconds=60*5 + random.randrange(0, 60*5))
		db_sess.commit()
		return
	else:
		with FETCH_LOCK:
			ACTIVE_FETCHES[job.netloc] += 1
		engine.do_job(job)
		time.sleep(5)
		with FETCH_LOCK:
			ACTIVE_FETCHES[job.netloc] -= 1



dispatchers = {
	'so_remote_fetch' : handleSoRemoteFetch,
	# 'remote_fetch'    : handleRemoteFetch,
	'remote_fetch'    : handleSoRemoteFetch,
	'rate_limit'      : handleRateLimiting,

}


def doSpecialCase():
	'''
	Handle processing AMQP queue responses here.
	Return true if there was a queue responseto handle, false if there was not.
	'''
	had_job = False

	return had_job

def handleSpecialCase(job, engine, rules, db_sess):
	commands = rules[job.netloc]
	op, params = commands[0], commands[1:]
	if op in dispatchers:
		return dispatchers[op](params, job, engine, db_sess)
	else:
		log.error("Error! Unknown special-case filter!")
		print("Filter name: '%s', parameters: '%s', job URL: '%s'", op, params, job.url)

def test():
	pass

if __name__ == '__main__':
	test()



