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
			else:
				print("No tmp:", tmp, x)
				time.sleep(1)
		except queue.Empty:
			time.sleep(1)


def process_resolver_response(resp):
	pprint.pprint(resp)
	if 'traceback' in resp:
		print()
		print("Exception!")
		for line in resp['traceback']:
			print(line)
	extradat = resp['extradat']
	if 'ret' in resp:
		for item in resp['ret']:
			item_guid = extradat[item['extra-info']['original_url']]
			meta = common.rss_func_db.get_feed_article_meta(item_guid)
			meta['ad_free'] = item['extra-info']['ad_free']
			if 'resolved_url' in item['extra-info']:
				meta['resolved_url'] = item['extra-info']['resolved_url']
			common.rss_func_db.set_feed_article_meta(item_guid, meta)



def _build_qidian_resolver_job(url_list, extradat=None):
	if extradat is None:
		extradat = {}

	qidianProcessReleaseList_job_data = {
		'call': 'qidianProcessReleaseList',
		'dispatch_key': 'fetcher',
		'jobid': -1,
		'kwargs': {
			'feed_urls': [{'link' : tmp, 'title' : ""} for tmp in url_list],
		},
		'module': 'PreprocessFetch',
		'postDelay': 0,
		'serialize': True,
		'extradat': extradat,
		'args': []
	}

	return qidianProcessReleaseList_job_data

def _get_unqualified_urls():
	sess = common.database.get_db_session()
	feed = sess.query(common.database.RssFeedEntry) \
		.filter(common.database.RssFeedEntry.feed_name == "Qidian") \
		.scalar()

	print(feed)
	print(feed.feed_name)
	releases = list(feed.releases)
	print("Have %s releases" % len(releases))


	ret = []
	guid_url_map = {}
	for release in releases:
		meta = common.rss_func_db.get_feed_article_meta(release.contentid)
		if (not meta.get("ad_free", False)) or (not meta.get("resolved_url", False)):
			print(release, release.contenturl, meta, release.contentid,)
			ret.append(release.contenturl)
			guid_url_map[release.contenturl] = release.contentid
			if len(ret) > 100:
				return ret, guid_url_map

	return ret, guid_url_map

def exposed_process_unqualified_qidian_feed_items():

	urls, guid_url_map = _get_unqualified_urls()
	print(urls)


	rpc_interface = common.get_rpyc.RemoteJobInterface("Test_Interface!")
	rpc_interface.check_ok()
	print("RPC:", rpc_interface)

	raw_job = _build_qidian_resolver_job(urls, extradat=guid_url_map)

	print(raw_job)

	rpc_interface.put_job(raw_job)

	for x in range(60 * 15):

		try:
			tmp = rpc_interface.get_job()
			if tmp:
				print("response!")
				process_resolver_response(tmp)
			else:
				print("No tmp:", tmp, x)
				time.sleep(1)
		except queue.Empty:
			time.sleep(1)




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


