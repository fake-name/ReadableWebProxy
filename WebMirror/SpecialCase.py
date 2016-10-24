
if __name__ == '__main__':
	import logSetup
	logSetup.initLogging()

import logging
import datetime
import random
import common.database as db
import multiprocessing
import traceback
import time
import queue

random.seed()

ACTIVE_FETCHES = {
	# Populated at runtime
}

FETCH_LOCK       = multiprocessing.Lock()
RATE_LIMIT_ITEMS = {}


log = logging.getLogger("Main.Web.SpecialCaseHandler")



def handleRateLimiting(params, rid, joburl, netloc):
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



dispatchers = {
	'rate_limit'      : handleRateLimiting,
}


def getSpecialCase(specialcase):
	log.info("Special case handler checking for deferred fetches.")
	with FETCH_LOCK:
		print()
		print()
		print("RATE_LIMIT_ITEMS", RATE_LIMIT_ITEMS)
		print()
		print()
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


def pushSpecialCase(specialcase, rid, joburl, netloc):
	'''
	Handle processing AMQP queue responses here.
	Return true if there was a queue responseto handle, false if there was not.
	'''

	assert netloc in specialcase

	commands = specialcase[netloc]
	op, params = commands[0], commands[1:]

	if op in dispatchers:
		return dispatchers[op](params, rid, joburl, netloc)
	else:
		log.error("Error! Unknown special-case filter!")
		print("Filter name: '%s', parameters: '%s', job conf: '%s'", op, params, (rid, joburl, netloc))



def haveSpecialCase(specialcase, joburl, netloc):
	if netloc in specialcase:
		# No special case for netloc
		return True

	return False

def test():
	pass

if __name__ == '__main__':
	test()



