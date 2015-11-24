
import queue
import WebMirror.Engine


INITED = False

fetchers = queue.Queue()

# Only allow the engine queue to be built once.
def init_engines():
	if not INITED:
		INITED = True
		if not fetchers.qsize():
			for x in range(3):
				fetchers.put(WebMirror.Engine.SiteArchiver(cookie_lock=False, run_filters=False))

