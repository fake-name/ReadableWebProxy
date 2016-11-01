
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
