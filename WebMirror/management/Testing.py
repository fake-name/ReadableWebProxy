import time
import queue
import pprint
import urllib.parse
import sys
import random

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
import common.rss_func_db



def process_fetch_response(resp, sess):
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



def exposed_test_qidian_fetch():
	'''
	Trigger the qidian remote feed resolving system.
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
				process_fetch_response(tmp, sess)
				return
			else:
				print("No tmp:", tmp, x)
				time.sleep(1)
		except queue.Empty:
			time.sleep(1)

def exposed_load_urls_from_file(file_path):
	'''
	Load a file of URLs, and feed them through the URL filtering system.
	'''
	with open(file_path, "r") as fp:
		content = fp.readlines()
		content = [tmp.strip() for tmp in content]

	print(content)

	sess = common.database.get_db_session()
	c_lok = cookie_lock = multiprocessing.Lock()
	engine = WebMirror.Engine.SiteArchiver(cookie_lock=c_lok, new_job_queue=None, db_interface=sess)

	job = testJobFromUrl("https://www.webnovel.com/feed/")

	engine.upsertResponseLinks(job, plain=content, debug=True)

	print(engine)

def testJobFromUrl(url):
	netloc = urllib.parse.urlsplit(url).netloc
	return common.database.WebPages(
				state     = 'fetching',
				url       = url,
				starturl  = url,
				netloc    = netloc,
				distance  = common.database.MAX_DISTANCE-2,
				is_text   = True,
				priority  = common.database.DB_REALTIME_PRIORITY,
				type      = "unknown",
				fetchtime = datetime.datetime.now(),
				)


