

if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()

import common.database as db

import WebMirror.TimedTriggers.QueueTriggers
import pickle
import pprint

def exposed_print_scheduled_jobs():
	'''

	'''
	sess = db.get_db_session()

	items = sess.execute("""
		SELECT
			id, next_run_time , job_state
		FROM
			apscheduler_jobs
	""")
	items = list(items)
	for tid, nextcall, content in items:
		print("Job: ", tid.ljust(30), str(nextcall).rjust(20))

		dat = pickle.loads(content)
		pprint.pprint(dat)
