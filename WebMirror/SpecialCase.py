
import logging
import datetime
import random
import WebMirror.database as db
import multiprocessing
import time
random.seed()

ACTIVE_FETCHES = {
	# Populated at runtime
}

FETCH_LOCK = multiprocessing.Lock()

log = logging.getLogger("Main.Web.SpecialCaseHandler")


def handleRemoteFetch(params, job, engine, db_sess):
	# print("Remote fetch command!")
	pass

def handleSoRemoteFetch(params, job, engine, db_sess):
	# print("Remote fetch command!")
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
	import logSetup
	logSetup.initLogging()



