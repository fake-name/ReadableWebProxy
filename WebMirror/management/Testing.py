import time
import queue
import pprint

import datetime
import common.database
import feedparser


import logSetup
import WebMirror.rules
import WebMirror.Engine
import common.database
import multiprocessing

import common.get_rpyc
import WebMirror.SpecialCase

def exposed_test_qidian_fetch():
	'''

	'''

	sess = common.database.get_db_session()

	rpc_interface = common.get_rpyc.RemoteJobInterface("Test_Interface!")
	rpc_interface.check_ok()
	print("RPC:", rpc_interface)

	print("Dispatching job engine")

	WebMirror.SpecialCase.qidianSmartFeedFetch(None, -1, 'https://www.webnovel.com/feed/', None, job_aggregator_instance=rpc_interface)

	for x in range(60 * 15):

		try:
			tmp = rpc_interface.get_job()
			if tmp:
				print("response!")
				process_response(tmp, sess)
			else:
				print("No tmp:", tmp, x)
				time.sleep(1)
		except queue.Empty:
			time.sleep(1)


def process_response(resp, sess):
	pprint.pprint(resp)
	if 'traceback' in resp:
		print()
		print("Exception!")
		for line in resp['traceback']:
			print(line)

	if 'ret' in resp:

		c_lok = cookie_lock = multiprocessing.Lock()
		engine = WebMirror.Engine.SiteArchiver(cookie_lock=c_lok, new_job_queue=None, db_interface=sess)
		print("Dispatching resp ret")
		engine.dispatchRequest(testJobFromUrl('https://www.webnovel.com/feed/'), resp['ret'])



def exposed_test_qidian_feed_proc(dpath):
	sess = common.database.get_db_session()
	with open(dpath) as fp:
		content = fp.read()

	resp = (content, "",  'application/rss+xml')
	c_lok = cookie_lock = multiprocessing.Lock()
	engine = WebMirror.Engine.SiteArchiver(cookie_lock=c_lok, new_job_queue=None, db_interface=sess)
	print("Dispatching resp ret")
	engine.dispatchRequest(testJobFromUrl('https://www.webnovel.com/feed/'), resp)




def testJobFromUrl(url):
	return common.database.WebPages(
				state     = 'fetching',
				url       = url,
				starturl  = url,
				netloc    = "wat",
				distance  = common.database.MAX_DISTANCE-2,
				is_text   = True,
				priority  = common.database.DB_REALTIME_PRIORITY,
				type      = "unknown",
				fetchtime = datetime.datetime.now(),
				)


