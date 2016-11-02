
import queue
import pprint
import traceback

from sqlalchemy.orm import joinedload

import runStatus
import common.database as db
import common.RunManager
import common.get_rpyc
import common.util.webFunctions
from WebMirror.NewJobQueue import buildjob
from . import NuSeriesPageFilter

def get_message_queue():
	pass



def print_response(resp):
	print("Response: ")
	pprint.pprint(resp)
	if not resp:
		print("Respone is None!")
		return
	if "traceback" in resp:
		pprint.pprint(resp['traceback'])

def exposed_head(url, ref):
	'''
	Do a phantomjs HEAD request for url `url`, passing the referrer `ref`
	'''

	rpc_interface = common.get_rpyc.RemoteJobInterface("Test_Interface!")
	print('wat?')
	print(rpc_interface)


	raw_job = buildjob(
		module         = 'NUWebRequest',
		call           = 'getHeadPhantomJS',
		dispatchKey    = "fetcher",
		jobid          = -1,
		args           = [url, ref],
		kwargs         = {},
		additionalData = {'mode' : 'fetch'},
		postDelay      = 0,
		unique_id      = url
	)

	rpc_interface.put_job(raw_job)
	while True:
		try:
			resp = rpc_interface.get_job()
			print_response(resp)

		except queue.Empty:
			print("No response yet?")

def exposed_cross_sync_nu_feeds():
	'''
	Re-synchronize the NU feed items from the old system (NuOutboundWrapperMap)
	to the new NuReleaseItem/NuResolvedOutbound pair mechanism.
	'''

	# client_id
	# client_key

	sess = db.get_db_session()
	print("Loading extant rows...")
	old_nu_items = sess.query(db.NuOutboundWrapperMap).all()
	print("Loaded. Processing")
	have_count = 0
	new_count  = 0
	loops = 0

	for old_nu in old_nu_items:
		have = sess.query(db.NuReleaseItem)                                     \
			.options(joinedload('resolved'))                                    \
			.filter(db.NuReleaseItem.outbound_wrapper==old_nu.outbound_wrapper) \
			.scalar()
		if not have:
			have = db.NuReleaseItem(
					validated        = old_nu.validated,
					seriesname       = old_nu.seriesname,
					releaseinfo      = old_nu.releaseinfo,
					groupinfo        = old_nu.groupinfo,
					referrer         = old_nu.referrer,
					outbound_wrapper = old_nu.outbound_wrapper,
					first_seen       = old_nu.released_on,
					actual_target    = old_nu.actual_target,
				)
			sess.add(have)
			loops += 1
			new_count += 1


		old_key = (old_nu.client_id, old_nu.client_key, old_nu.actual_target)
		resolved = set([(itm.client_id, itm.client_key, itm.actual_target) for itm in have.resolved])
		if not old_key in resolved:
			new = db.NuResolvedOutbound(
					client_id      = old_nu.client_id,
					client_key     = old_nu.client_key,
					actual_target  = old_nu.actual_target,
					fetched_on     = old_nu.released_on,
				)
			have.resolved.append(new)
			loops += 1
			new_count += 1
			print("New release!")
		else:
			have_count += 1

		if loops == 100:
			print("Commit! Have {}, new {}".format(have_count, new_count))
			sess.commit()
			loops = 0

		# for chunk in have.resolved:
		# 	print(chunk)

def exposed_process_nu_pages(transmit=True):
	'''
	Re-process all locally saved novelupdates pages.
	'''


	wg = common.util.webFunctions.WebGetRobust()
	sess = db.get_db_session()

	if transmit == True:
		rm = common.RunManager.Crawler(1, 1)
		message_q = rm.start_aggregator()
	else:
		message_q = queue.Queue()

	pages = []
	for row in sess.query(db.WebPages) \
		.filter(db.WebPages.netloc == "www.novelupdates.com") \
		.yield_per(50).all():

		rowtmp = {
			"pageUrl"   : row.url,
			"pgContent" : row.content,
			"type"      : row.mimetype,
			"wg"        : wg,
			"message_q" : message_q,
		}
		pages.append(rowtmp)

		if len(pages) == 100:
			print("Loaded %s pages..." % len(pages))
	sess.flush()
	sess.commit()
	for row in pages:
		try:
			# print(row, row.url, row.state)
			if row['pgContent'] and NuSeriesPageFilter.NUSeriesPageProcessor.wantsUrl(row['pageUrl']):
				proc = NuSeriesPageFilter.NUSeriesPageProcessor(db_sess=sess, **row)
				proc.extractContent()
		except Exception:
			print("")
			print("ERROR!")
			for line in traceback.format_exc().split("\n"):
				print(line.rstrip())
			print("")
		except KeyboardInterrupt:
			break

	runStatus.run_state.value = 0

	if transmit == True:
		rm.join_aggregator()

	print(sess)
