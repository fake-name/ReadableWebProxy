
import calendar
import datetime
import json
import os
import os.path
import shutil
import tqdm
import traceback
from concurrent.futures import ThreadPoolExecutor

import urllib.error
import urllib.parse

from sqlalchemy import and_
from sqlalchemy import or_
import sqlalchemy.exc

if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()

import common.database as db
import common.Exceptions
import common.management.util
import common.management.file_cleanup
import common.management.WebMirrorManage


import WebMirror.processor.RssProcessor
import flags
import pprint
import config
from config import C_RAW_RESOURCE_DIR

import WebMirror.OutputFilters.rss.FeedDataParser

import WebMirror.OutputFilters.util.feedNameLut
import common.util.WebRequest



def exposed_fix_lndb_urls():
	'''
	Scan the qidian feed items, and extract the book url segments which are not
	in the feedparser url-seg -> title map.

	Given those segments, then do a HTTP fetch, and pull out the page title.
	Finally, print that information in a nice table for updating the
	scraper func.
	'''

	with db.session_context() as sess:

		pages = sess.query(db.WebPages) \
				.filter(db.WebPages.netloc == "lndb.info")    \
				.all()

		print(pages)


		# feed_url = feed_item.urls[0].feed_url
		# pfunc = feed_item.get_func()

		# missing = []

		# for release in feed_item.releases:
		# 	item = {}
		# 	item['title']    = release.title
		# 	item['guid']     = release.contentid
		# 	item['linkUrl']  = release.contenturl

		# 	item['feedUrl']  = feed_url
		# 	item['srcname']  = "wat"
		# 	item['published']  = "wat"

		# 	ret = pfunc(item)
		# 	if not ret:
		# 		missing.append(release.contenturl)

		# urls = {}
		# for url in missing:
		# 	root, _ = url.rsplit("/", 1)
		# 	urls[root] = url

		# wg = common.util.WebRequest.WebGetRobust()

		# lines = []
		# for root, url in urls.items():
		# 	urlfrag = root.split("www")[-1]
		# 	meta = common.management.util.get_page_title(wg, url)
		# 	title =  meta['title']
		# 	outstr = "		('www{}/', '{}', 'translated'),".format(urlfrag, title)
		# 	lines.append(outstr)

		# for outstr in lines:
		# 	print(outstr)



def exposed_fix_nu_duplicate_url_segments():
	'''
	So the novelupdate scrape borked somewhere, and is generating duplicate URLs.

	Gah.
	'''

	with db.session_context() as sess:
		print("Querying for rows")
		res = sess.query(db.NuReleaseItem.id, db.NuReleaseItem.outbound_wrapper).all()
		print("Found %s nu outbound wrappers" % len(res))

	total = 0
	bad = 0
	urlmap = {}
	fix_list = []
	print("Parsing URLs")
	for dbid, url in res:
		total += 1
		if url.count("http") > 1:
			bad += 1
			fix_list.append((dbid, url))
			# print(dbid, url)
		else:
			urlmap[url] = dbid

	print("Found %s links, %s of which are invalid" % (total, bad))

	count = 0
	with db.session_context() as sess:
		for dbid, url in tqdm.tqdm(fix_list):
			actual_url, _ = url.split("http://")

			if actual_url in urlmap:
				res = sess.query(db.NuResolvedOutbound).filter_by(parent=dbid).update({"parent" : urlmap[actual_url]})
				res = sess.query(db.NuReleaseItem).filter_by(id=dbid).delete()
			else:
				res = sess.query(db.NuReleaseItem).filter_by(id=dbid).update({"outbound_wrapper" : actual_url})

				urlmap[url] = dbid
			count += 1
			if count > 2500:
				count = 0
				sess.commit()
			# res = sess.query(db.NuReleaseItem.id, db.NuReleaseItem.outbound_wrapper).all()

		sess.commit()
		# print(dbid, curl)

