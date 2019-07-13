
import queue
import pprint
import time
import datetime
import traceback

from sqlalchemy.orm import joinedload
from sqlalchemy import not_

import runStatus
import common.database as db
import common.RunManager
import common.get_rpyc
import WebRequest
from WebMirror.JobUtils import buildjob
from WebMirror.OutputFilters.Nu import NuSeriesPageFilter

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
		module         = 'SmartWebRequest',
		call           = 'getHeadTitleChromium',
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
	'''
	Process received NU head values, and if a row has three or more
	received head responses that match, mark them as validated and
	timestamp them.
	'''

	hd = Misc.NuForwarder.NuHeader.NuHeader()
	hd.validate_from_new()
	hd.timestamp_validated()

def exposed_drain_nu_responses():
	'''
	Block indefinitely while waiting for NU head responses in the amqp queue system.
	'''

	hd = Misc.NuForwarder.NuHeader.NuHeader()
	while 1:
		hd.process_avail()
		time.sleep(1)


def exposed_do_nu_head():
	'''
	Execute the NU header system with 50 available urls, and
	then wait 2 minutes for the responses to come back.

	'''

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



def exposed_delete_old_nu_root_outbound():
	'''
	Delete NU outbound links that use the homepage as their referrer.

	Apparently NU was validating the referrer to see if the referring page actually had
	the referring link on it, or /something/.

	Anyways, it's easier to generate a permanent referrer by just pointing it at
	the series page.
	'''


	with db.session_context() as sess:

		for row in sess.query(db.NuReleaseItem) \
			.filter(not_(db.NuReleaseItem.referrer.like("%novelupdates.com/series%"))) \
			.yield_per(50).all():
			if not len(list(row.resolved)):
				print(row.id, row.referrer)
				sess.delete(row)
				sess.commit()

def exposed_delete_nu_unresolved():
	'''
	Delete all nu head system rows that have not been reviewed.

	This is needed for historical purges, particularly if
	nu changes their extnu ids, or if the url masking
	mechanism has significant changes.
	'''
	with db.session_context() as sess:

		count = 0
		print("Loading rows....")
		rows = sess.query(db.NuReleaseItem) \
			.options(joinedload('resolved'))    \
			.all()
		print("Loaded %s rows. Scanning." % len(rows))
		for row in rows:

			if len(list(row.resolved)) == 0 and row.reviewed == 'unverified':

				print(row.id, len(list(row.resolved)), row.referrer)
				for bad in row.resolved:
					sess.delete(bad)
				sess.delete(row)
				count += 1
				if count % 500 == 0:
					print("Committing!")
					sess.commit()

		print("Committing!")
		sess.commit()



def exposed_process_nu_pages(transmit=True):
	'''
	Re-process all locally saved novelupdates pages.
	'''


	wg = WebRequest.WebGetRobust()
	with db.session_context() as sess:

		if transmit == True:
			print("Transmitting processed results")
			rm = common.RunManager.Crawler(1, 1)
			message_q = rm.start_aggregator()
		else:
			print("Not translating processed results")
			message_q = queue.Queue()

		pages = []
		print("Beginning DB retreival")
		for row in sess.query(db.WebPages) \
			.filter(db.WebPages.netloc == "www.novelupdates.com") \
			.filter(db.WebPages.url.ilike("%/series/%")) \
			.yield_per(50).all():

			rowtmp = {
				"pageUrl"   : row.url,
				"pgContent" : row.content,
				"type"      : row.mimetype,
				"wg"        : wg,
				"message_q" : message_q,
			}
			pages.append(rowtmp)

			if len(pages) % 100 == 0:
				print("Loaded %s pages..." % len(pages))
		sess.flush()
		sess.commit()
		for row in pages:
			try:
				# print(row, row.url, row.state)
				if row['pgContent'] and NuSeriesPageFilter.NUSeriesPageFilter.wantsUrl(row['pageUrl']):
					proc = NuSeriesPageFilter.NUSeriesPageFilter(db_sess=sess, **row)
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



def exposed_retransmit_nu_releases(all_releases=False):
	'''
	If all_releases is not specified, the last one day of releases are sent.
	If all_releases is present, all releases ever received are sent.
	Transmit all validated NU items through the RabbitMQ update feed system.
	'''

	header = Misc.NuForwarder.NuHeader.NuHeader()
	print(header)

	if all_releases is False:
		ago = datetime.datetime.now() - datetime.timedelta(days=1)
		header.transmit_since(earliest=ago)
	else:
		header.transmit_since()



def exposed_get_nu_releases_with_dots():
	'''
	Get the nu releases that aren't transmittable (as they're truncated)
	'''

	header = Misc.NuForwarder.NuHeader.NuHeader()

	header.get_dotted()
