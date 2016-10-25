
import queue
import traceback
import runStatus
import common.database as db
import common.RunManager
import common.util.webFunctions

from . import NuSeriesPageFilter

def get_message_queue():
	pass

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

	for row in sess.query(db.WebPages) \
		.filter(db.WebPages.netloc == "www.novelupdates.com") \
		.yield_per(1000).all():
		try:
			# print(row, row.url, row.state)
			if row.content and NuSeriesPageFilter.NUSeriesPageProcessor.wantsUrl(row.url):
				print(row)
				proc = NuSeriesPageFilter.NUSeriesPageProcessor(
						pageUrl   = row.url,
						pgContent = row.content,
						type      = row.mimetype,
						wg        = wg,
						db_sess   = sess,
						message_q = message_q,
					)
				proc.extractContent()
				print(proc)
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
