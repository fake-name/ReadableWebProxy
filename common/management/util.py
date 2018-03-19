
import pickle
import urllib.parse
import pprint
import WebRequest

if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()

import common.database as db


def get_page_title(wg, url):
	ret = {}
	ret['title'] = urllib.parse.urlsplit(url).netloc

	try:
		soup = wg.getSoup(url)
		ret['is-wp'] = "/wp-content/" in str(soup)
		if soup.title:
			ret['title'] = soup.title.get_text().strip()
	except WebRequest.FetchFailureError as err:
		ret['failed'] = True
		ret['code'] = err.err_code
		ret['reason'] = err.err_reason
		ret['err'] = str(err)

	except Exception as err:
		ret['failed'] = True
		ret['err'] = err

	return ret
