

if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()

import common.database as db

import WebMirror.TimedTriggers.QueueTriggers
import pickle
import urllib.parse
import pprint

def get_page_title(wg, url):
	ret = {}
	ret['title'] = urllib.parse.urlsplit(url).netloc

	try:
		soup = wg.getSoup(url)
		ret['is-wp'] = "/wp-content/" in str(soup)
		if soup.title:
			ret['title'] = soup.title.get_text().strip()
	except Exception:
		pass

	return ret
