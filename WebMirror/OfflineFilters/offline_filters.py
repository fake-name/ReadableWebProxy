
import queue
import pprint
import time
import traceback

from sqlalchemy.orm import joinedload
from sqlalchemy import desc
from sqlalchemy import not_
import sqlalchemy.exc

import runStatus
import common.database as db
import common.RunManager
import common.get_rpyc
import common.util.webFunctions
from WebMirror.NewJobQueue import buildjob
from . import NuSeriesPageFilter

import Misc.NuForwarder.NuHeader

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
			if not resp:
				time.sleep(1)

		except queue.Empty:
			print("No response yet?")

def exposed_update_nu_responses():

	hd = Misc.NuForwarder.NuHeader.NuHeader()
	hd.validate_from_new()
	hd.timestamp_validated()

def exposed_drain_nu_responses():

	hd = Misc.NuForwarder.NuHeader.NuHeader()
	while 1:
		hd.process_avail()
		time.sleep(1)


def exposed_do_nu_head():
	'''
	'''
	# Misc.NuForwarder.NuHeader.fetch_and_flush()

	while 1:
		hd = Misc.NuForwarder.NuHeader.NuHeader()

		jobcnt = 50
		print("Putting %s jobs!" % jobcnt)
		hd.put_job(put=jobcnt)

		sleep_for = 120
		try:
			for x in range(sleep_for):
				hd.process_avail()
				time.sleep(1)
				print("Sleeping %s of %s" % (x, sleep_for))
		except KeyboardInterrupt:
			print("Interrupted!")
			return
		exposed_update_nu_responses()


def exposed_confirm_from_heads():
	sess = db.get_db_session()
	print("Loading extant rows...")
	have = sess.query(db.NuReleaseItem)                                     \
		.options(joinedload('resolved'))                                    \
		.all()
	print("Loaded. Processing")

	for row in have:
		res = list(row.resolved)
		if res:
			print(len(res))


def cross_sync(increment):

	sess = db.get_db_session()
	print("Loading extant rows...")
	old_nu_items = sess.query(db.NuOutboundWrapperMap).order_by(desc(db.NuOutboundWrapperMap.id)).all()
	print("Loaded. Processing")
	have_count = 0
	new_count  = 0
	loops = 0
	nc_loops = 0
	try:

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
			else:
				have_count += 1
				nc_loops += 1

			if loops > increment:
				print("Commit! Have {}, new {} ({}, {})".format(have_count, new_count, loops, nc_loops))
				sess.commit()
				loops = 0

			if nc_loops > 100:
				print("Have {}, new {} ({}, {})".format(have_count, new_count, loops, nc_loops))
				nc_loops = 0
		sess.commit()
	except Exception:
		sess.rollback()
		raise

def exposed_cross_sync_nu_feeds():
	'''
	Re-synchronize the NU feed items from the old system (NuOutboundWrapperMap)
	to the new NuReleaseItem/NuResolvedOutbound pair mechanism.
	'''

	# client_id
	# client_key
	increment = 51
	while 1:
		try:
			cross_sync(increment=increment)
			return
		except sqlalchemy.exc.IntegrityError:
			increment = max(1, increment-25)


def exposed_delete_old_nu_root_outbound():
	sess = db.get_db_session()

	for row in sess.query(db.NuReleaseItem) \
		.filter(not_(db.NuReleaseItem.referrer.like("%novelupdates.com/series%"))) \
		.yield_per(50).all():
		if not len(list(row.resolved)):
			print(row.id, row.referrer)
			sess.delete(row)
			sess.commit()



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
