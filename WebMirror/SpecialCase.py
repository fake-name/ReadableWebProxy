
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
		for line in traceback.format_exc().split("\n"):
			log.error(line)

		raise RuntimeError("Cannot stop AMQP fetcher that is not running!!")

	AMQP_FETCHER.close()
	del AMQP_FETCHER
	AMQP_FETCHER = None


def handleRemoteFetch(params, job, engine, db_sess):
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
			postDelay      = 0
		)


	AMQP_FETCHER.put_job(raw_job)

def doRemoteHead(url, referrer):
	# remote_fetch, WebRequest, getItem
	raw_job = AmqpHandler.buildjob(
			module         = 'WebRequest',
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


	AMQP_FETCHER.put_job(raw_job)


def blockingRemoteHead(url, referrer):

	timeout = 60 # 60 seconds.
	db_sess = db.get_db_session()

	transmitted = False

	for x in range(timeout):
		row =  db_sess.query(db.NuOutboundWrapperMap)                    \
			.filter(db.NuOutboundWrapperMap.container_page == referrer ) \
			.filter(db.NuOutboundWrapperMap.link_url       == url )      \
			.scalar()
		if row:
			return row.target_url
		if not transmitted:
			transmitted = True
			doRemoteHead(url, referrer)
		time.sleep(1)

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
	'remote_fetch'    : handleRemoteFetch,
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
		dispatchers[op](params, job, engine, db_sess)
	else:
		log.error("Error! Unknown special-case filter!")
		print("Filter name: '%s', parameters: '%s', job URL: '%s'", op, params, job.url)

def test():
	pass

if __name__ == '__main__':
	test()



