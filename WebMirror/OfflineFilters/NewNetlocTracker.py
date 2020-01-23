
import sys
import time
import datetime
import traceback
import urllib.parse

import tqdm

from sqlalchemy.orm import joinedload
from sqlalchemy import desc

import WebRequest

import common.database as db
import common.management.util
import common.global_constants
import common.util.urlFuncs as urlFuncs

import WebMirror.OutputFilters.util.feedNameLut
import WebMirror.rules


def get_wln_release_urls():
	'''
	Exec time: ~60-70 seconds
	'''

	print("loading netlocs from WLN release listings")

	import settings

	if '__pypy__' in sys.builtin_module_names:
		import psycopg2cffi as psycopg2
	else:
		import psycopg2

	conn = psycopg2.connect(
			host     = settings.WLN_DB_DATABASE_IP,
			dbname   = settings.WLN_DB_DATABASE_DB_NAME,
			user     = settings.WLN_DB_DATABASE_USER,
			password = settings.WLN_DB_DATABASE_PASS,
		)

	print("Conn:", conn)
	cur = conn.cursor()

	print("Fetching rows from changes table")
	cur.execute("""
		SELECT DISTINCT(srcurl) FROM releaseschanges;
		""")
	rows_1 = cur.fetchall()
	print("Fetching rows from main table")
	cur.execute("""
		SELECT DISTINCT(srcurl) FROM releases;
		""")

	rows_2 = cur.fetchall()
	print("Received %s, %s distinct URLs" % (len(rows_1), len(rows_2)))

	nlfilter = {}
	for url, in tqdm.tqdm(rows_1 + rows_2):
		if url:
			if isinstance(url, bytes):
				url = url.decode("utf-8")
			itemnl = WebMirror.OutputFilters.util.feedNameLut.patch_blogspot(urllib.parse.urlsplit(url).netloc)
			nlfilter.setdefault(itemnl, set())
			nlfilter[itemnl].add(url)

	print("WLN Releases distinct netlocs: %s" % len(nlfilter))

	return nlfilter

def get_nu_head_urls():
	'''
	Exec time: ~3.5 seconds
	'''

	print("Loading netlocs from nuheader system")
	with db.session_context() as sess:

		nu_items = sess.query(db.NuReleaseItem)             \
			.filter(db.NuReleaseItem.actual_target != None) \
			.all()

		mapdict = {}
		for row in nu_items:
			itemnl = WebMirror.OutputFilters.util.feedNameLut.patch_blogspot(urllib.parse.urlsplit(row.actual_target).netloc)
			mapdict.setdefault(itemnl, set())
			mapdict[itemnl].add(row.actual_target)


	print("Nu outbound items: ", len(mapdict))

	return mapdict



def get_distance_of_zero_urls():
	'''
	Exec time: ~80-90  seconds
	'''
	print("Loading short-distance netlocs")
	with db.session_context() as sess:

		page_items = sess.query(db.WebPages.url)                \
			.filter(db.WebPages.distance <= db.DB_DEFAULT_DIST) \
			.filter(db.WebPages.is_text  == True)               \
			.yield_per(10000)                                   \
			.all()

		mapdict = {}
		for row, in tqdm.tqdm(page_items):
			itemnl = WebMirror.OutputFilters.util.feedNameLut.patch_blogspot(urllib.parse.urlsplit(row).netloc)
			mapdict.setdefault(itemnl, set())
			mapdict[itemnl].add(row)


	print("short-distance items: ", len(mapdict))

	return mapdict


def filter_get_have_urls():

	rules = WebMirror.rules.load_rules()
	urls = [item['starturls'] if item['starturls'] else [] + item['feedurls'] if item['feedurls'] else [] for item in rules]
	urls = [item for sublist in urls for item in sublist]

	start_netloc_dict = {}

	for url in urls:
		itemnl = WebMirror.OutputFilters.util.feedNameLut.patch_blogspot(urllib.parse.urlsplit(url).netloc)
		start_netloc_dict.setdefault(itemnl, [])
		start_netloc_dict[itemnl] = url


	missing = 0

	with db.session_context() as sess:
		rows = sess.query(db.NewNetlocTracker)  \
			.filter(db.NewNetlocTracker.ignore == False) \
			.filter(db.NewNetlocTracker.have == False) \
			.all()

		for row in tqdm.tqdm(rows):

			if not row.netloc:
				print("What:", (row.id, row.example_url, row.netloc))
				sess.delete(row)
				sess.commit()
				continue

			assert row.netloc

			netloc = row.netloc.lower()
			bad = False

			if urlFuncs.SQUATTER_NETLOC_RE.match(netloc):
				bad = True

			if netloc in common.global_constants.NU_NEW_MASK_NETLOCS:
				bad = True

			if netloc.endswith(".photobucket.com"):
				bad = True
			if netloc.endswith(".postimg.org"):
				bad = True

			if "www.novelupdates.com" in netloc:
				bad = True

			if netloc.endswith("files.wordpress.com"):
				bad = True
			if netloc.endswith("media.tumblr.com"):
				bad = True
			if netloc.endswith("bp.blogspot.com"):
				bad = True

			if WebMirror.OutputFilters.util.feedNameLut.getNiceName(sess, srcurl=None, netloc=netloc):
				row.ignore = False
				row.have = True
				sess.commit()
				continue


			# Try to check www./non-www. URLs
			if netloc.startswith("www."):
				if WebMirror.OutputFilters.util.feedNameLut.getNiceName(sess, srcurl=None, netloc=netloc[4:]):
					bad = True

			if netloc in start_netloc_dict:
				row.ignore = False
				row.have = True
				sess.commit()
				continue

			if bad:
				row.ignore = True
				sess.commit()
				continue

			# print("Missing: ", (netloc, title, random_nl))
			missing += 1

		total = len(rows)

	print("Total outbound items: ", total, "missing:", missing)


def update_missing_new_with_title():

	wg = WebRequest.WebGetRobust()

	with db.session_context() as sess:
		rows = sess.query(db.NewNetlocTracker)  \
			.filter(db.NewNetlocTracker.ignore == False) \
			.filter(db.NewNetlocTracker.have == False) \
			.all()

		print("Missing items:", len(rows))

		for row in tqdm.tqdm(rows):
			if row.extra is None:
				row.extra = {}
			if not 'title' in row.extra:
				titledict = common.management.util.get_page_title(wg, row.example_url)
				for key, value in titledict.items():
					row.extra[key] = value
				sess.commit()


def get_high_priority_urls(filter_before=None):
	'''
	Exec time: ~0.2 seconds
	'''
	print("Loading high priority netlocs")
	with db.session_context() as sess:

		query = sess.query(db.WebPages.url)                      \
			.filter(db.WebPages.priority <= db.DB_HIGH_PRIORITY) \
			.filter(db.WebPages.is_text  == True)                \
			.yield_per(10000)

		if filter_before:
			query = query.filter(db.NuReleaseItem.release_date >= filter_before)

		page_items = query.all()

		mapdict = {}
		for row, in tqdm.tqdm(page_items):
			itemnl = WebMirror.OutputFilters.util.feedNameLut.patch_blogspot(urllib.parse.urlsplit(row).netloc)
			mapdict.setdefault(itemnl, set())
			mapdict[itemnl].add(row)


	print("High Priority outbound items: ", len(mapdict))

	return mapdict

def push_urls_into_table(mapdict):
	with db.session_context() as db_sess:
		pbar = tqdm.tqdm(mapdict.items())
		for netloc, urls in pbar:
			have_item = db_sess.query(db.NewNetlocTracker)        \
				.filter(db.NewNetlocTracker.netloc == netloc) \
				.scalar()

			if not have_item and netloc:
				urls = list(urls)
				urls.sort(key=lambda x:len(x))

				pbar.write("New Url: %s -> %s" % (netloc, urls[0]))

				new = db.NewNetlocTracker(
						netloc      = netloc,
						example_url = urls[0],
					)
				db_sess.add(new)
				db_sess.commit()



def reset_nu_fails():

	with db.session_context() as db_sess:
		recent_d_2 = datetime.datetime.now() - datetime.timedelta(hours=24*14)
		bulkq = db_sess.query(db.NuReleaseItem)                       \
			.outerjoin(db.NuResolvedOutbound)                         \
			.filter(db.NuReleaseItem.validated == False)              \
			.filter(db.NuReleaseItem.release_date >= recent_d_2)      \
			.options(joinedload('resolved'))                          \
			.order_by(desc(db.NuReleaseItem.first_seen))              \

		items   = bulkq.all()

		print("Found %s items." % len(items))

		for item in items:
			resolved = len(item.resolved)
			item.fetch_attempts = resolved
			# print("Item has %s resolves, %s attempts" % (len(item.resolved), item.fetch_attempts))

		db_sess.commit()


######################################################################################################################################################
# Exposed functions
######################################################################################################################################################


def exposed_new_from_wln_feeds():
	'''
	Parse the local WLN instance's release listing and extract the found release urls
	that are not in the known feednamelut.
	'''
	nlfilter = get_wln_release_urls()
	push_urls_into_table(mapdict)


def exposed_new_from_nu_feeds():
	'''
	Parse outbound netlocs from NovelUpdates releases, extracting
	any sites that are not known in the feednamelut.
	'''

	mapdict = get_nu_head_urls()
	push_urls_into_table(mapdict)

def exposed_new_from_high_priority():
	'''
	Parse rows from main DB which have a high priority setting, extracting
	any sites that are not known in the feednamelut.
	'''

	mapdict = get_high_priority_urls()
	push_urls_into_table(mapdict)

def exposed_new_from_zero_distance_urls():
	'''
	Parse rows from main DB which have a fetch distance of 0, extracting
	any sites that are not known in the feednamelut.
	'''

	mapdict = get_distance_of_zero_urls()
	push_urls_into_table(mapdict)

def exposed_new_from_all_feeds():
	'''
	Parse outbound netlocs from NovelUpdates and WLN releases, extracting
	any sites that are not known in the feednamelut.
	'''

	mapdict = get_nu_head_urls()
	mapdict_1 = get_wln_release_urls()
	mapdict_2 = get_high_priority_urls()
	mapdict_3 = get_distance_of_zero_urls()

	print("NU Header urls: %s, wln URLs: %s, %s high priority items, %s with a distance of zero." % (len(mapdict), len(mapdict_1), len(mapdict_2), len(mapdict_3)))

	for key, value in mapdict_1.items():
		mapdict.setdefault(key, set())
		mapdict[key].update(value)

	for key, value in mapdict_2.items():
		mapdict.setdefault(key, set())
		mapdict[key].update(value)

	for key, value in mapdict_3.items():
		mapdict.setdefault(key, set())
		mapdict[key].update(value)

	print("Total items: %s" % (len(mapdict), ))

	push_urls_into_table(mapdict)

def exposed_process_urls_from_netloc_tracker(fetch_title=False):
	'''
	Process items from the netloc tracker table.
	'''

	filter_get_have_urls()

	if fetch_title:
		update_missing_new_with_title()

def exposed_update_missing_new_with_title():
	'''
	Fetch titles from the new-netloc entry items which are new and not marked as ignore
	'''
	update_missing_new_with_title()

######################################################################################################################################################


def exposed_reset_nu_fetch_failures():
	'''
	Reset nu head fetch counts to the number of actual fetches received.
	'''

	reset_nu_fails()
