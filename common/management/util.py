
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
		soupstr = str(soup)
		ret['is-wp'] = "/wp-content/" in soupstr
		ret['is-orig'] = '<strong class="pa t0 r0 z1">original</strong>' in soupstr
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

	if 'title' in ret and 'https://www.webnovel.com' in url:
		ret['title_orig'] = ret['title']
		ret['title'] = ret['title'].rsplit("-", 3)[0]
	return ret
