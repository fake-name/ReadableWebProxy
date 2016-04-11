
import queue
import WebMirror.Engine


INITED = False

fetchers = queue.Queue()
import WebMirror.database as db

# Only allow the engine queue to be built once.
def init_engines():
	global INITED
	if not INITED:
		INITED = True
		if not fetchers.qsize():
			for x in range(3):
				fetchers.put(WebMirror.Engine.SiteArchiver(cookie_lock=False, run_filters=False, db_interface=db.get_db_session()))

