
import datetime
import json
import os
import os.path
import sys
import tqdm
import pprint
import time
import random
import tqdm
import traceback
from concurrent.futures import ThreadPoolExecutor


import urllib.error
import urllib.parse

from sqlalchemy import and_
from sqlalchemy import desc
from sqlalchemy import or_
from sqlalchemy.sql import func
import sqlalchemy.exc
import sqlalchemy.orm.exc
from sqlalchemy_continuum_vendored.utils import version_table

if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()

from WebMirror.Engine import SiteArchiver
import WebMirror.OutputFilters.util.feedNameLut
import WebMirror.rules
import WebMirror.SiteSync.fetch
import WebMirror.SpecialCase
import WebMirror.JobDispatcher

import RawArchiver.RawActiveModules
import RawArchiver.RawEngine

import common.database as db
import common.Exceptions
import common.management.file_cleanup
import common.management.util
import common.global_constants
import WebRequest

import Misc.HistoryAggregator.Consolidate
import Misc.NuForwarder.NuHeader
import flags


from common.Exceptions import GarbageDomainSquatterException
import WebMirror.processor.HtmlProcessor
import WebMirror.TimedTriggers.RollingRewalkTriggers
import WebMirror.TimedTriggers.QueueTriggers
import WebMirror.SiteSync.fetch
import WebMirror.OutputFilters.rss.FeedDataParser



class TestQueueTrigger(WebMirror.TimedTriggers.QueueTriggers.QueueTrigger):

	loggerPath = 'TestTrigger'
	pluginName = 'TestTrigger'
	rpc_queue_name = 'TestInterface'

	def get_urls(self):
		return []


def get_job_from_url(sess, url, starturl, netloc):

	sess.flush()
	sess.commit()
	job = sess.query(db.WebPages) \
		.filter(db.WebPages.url == url)    \
		.scalar()
	sess.commit()

	if job:
		return job

	new = db.WebPages(
		url       = url,
		starturl  = starturl,
		netloc    = netloc,
		distance  = 5,
		is_text   = True,
		priority  = 9,
		type      = 'unknown',
		fetchtime = datetime.datetime.now(),
		)
	sess.add(new)
	sess.commit()

	return job




def exposed_remote_fetch_enqueue(url):
	'''
	Place a normal fetch request for url `url` into the remote fetch queue.

	Requires the FetchAgent service to be running.
	'''

	print("Enqueueing ")
	trig = WebMirror.TimedTriggers.QueueTriggers.NuQueueTrigger()
	trig.enqueue_url(url)

def exposed_remote_fetch_test(url):
	'''
	Place a normal fetch request for url `url` into the remote fetch queue,
	and then wait for the response.

	Requires the FetchAgent service to be running.
	'''

	print("Enqueueing ")
	trig = TestQueueTrigger()
	print(trig)
	trig.enqueue_url(url)

	for timeout in range(60 * 60):
		resp = trig.rpc_interface.get_job_nowait()
		print("\rLoop %s\r" % timeout, end='', flush=True)
		if resp:
			pprint.pprint(resp)
			return
		time.sleep(1)


def exposed_trigger_nu_homepage_fetch():
	'''
	Trigger testing for the QueueTrigger system
	'''
	trig = WebMirror.TimedTriggers.QueueTriggers.NuQueueTrigger()
	trig.go()

def exposed_do_nu_head_cycle():
	'''
	Do a fetch and wait for results session through the NU Header system.
	'''
	Misc.NuForwarder.NuHeader.fetch_and_flush()

def exposed_fetch_no_special_case(url, debug=True):
	'''
	Do a normal fetch() operation, but skip any special case filters.
	'''
	exposed_fetch(url, debug, special_case_enabled=False)

def exposed_fetch(url, debug=True, rss_debug=False, special_case_enabled=True):
	'''
	Do a synchronous fetch of content from url `url`.
	'''

	# try:
	# 	WebMirror.SpecialCase.startAmqpFetcher()
	# except RuntimeError:  # Fetcher already started
	# 	pass

	specialcase_data    = WebMirror.rules.load_special_case_sites()

	print("Debug: %s, rss_debug: %s" % (debug, rss_debug))
	if rss_debug:
		print("Debugging RSS")
		flags.RSS_DEBUG = True

	parsed = urllib.parse.urlparse(url)
	root = urllib.parse.urlunparse((parsed[0], parsed[1], "", "", "", ""))

	if WebMirror.SpecialCase.haveSpecialCase(specialcase_data, url, parsed.netloc) and special_case_enabled:
		WebMirror.SpecialCase.pushSpecialCase(specialcase_data, -1, url, parsed.netloc, None)
		return


	try:
		with db.session_context() as sess:


			archiver = SiteArchiver(None, sess, None)
			archiver.synchronousJobRequest(url, ignore_cache=True, debug=True)

	except Exception as e:
		traceback.print_exc()

def exposed_fetch_silent(tgt):
	'''
	Identical to `test_retrieve`, except debug printing is supressed.
	'''
	exposed_fetch(tgt, debug=False)


def exposed_raw_test_retrieve(url):
	'''
	Lower level fetch test, otherwise similar to `test_retreive`
	'''

	# try:
	# 	WebMirror.SpecialCase.startAmqpFetcher()
	# except RuntimeError:  # Fetcher already started
	# 	pass


	parsed = urllib.parse.urlparse(url)
	root = urllib.parse.urlunparse((parsed[0], parsed[1], "", "", "", ""))


	with db.session_context() as sess:

		row = sess.query(db.RawWebPages).filter(db.RawWebPages.url == url).scalar()
		if row:
			row.state = 'new'
		else:
			row = db.RawWebPages(
				url       = url,
				starturl  = root,
				netloc    = parsed.netloc,
				distance  = 50000,
				priority  = 500000,
				state     = 'new',
				fetchtime = datetime.datetime.now(),
				)
			sess.add(row)


		try:
			archiver = RawArchiver.RawEngine.RawSiteArchiver(
				total_worker_count = 1,
				worker_num         = 0,
				new_job_queue      = None,
				cookie_lock        = None,
				db_interface       = sess,
				response_queue     = None
				)
			archiver.do_job(row)
		except Exception as e:
			traceback.print_exc()

def exposed_longest_rows():
	'''
	Fetch the rows from the database where the `content` field is longest.
	Return is limited to the biggest 50 rows.
	VERY SLOW (has to scan the entire table)
	'''
	with db.session_context() as sess:
		print("Getting longest rows from database")
		have = sess.execute("""
			SELECT
				id, url, length(content), content
			FROM
				web_pages
			ORDER BY
				LENGTH(content) DESC NULLS LAST
			LIMIT 50000;
			""")
		print("Rows:")

		have = [list(tmp) for tmp in have]

		with open("Long_files.json", "w") as fp:
			json.dump(have, fp, indent=4)

		savepath = "./large_files/"
		for row in have[50:]:
			print(row[0], row[1])
			try:
				os.makedirs(savepath)
			except FileExistsError:
				pass
			with open(os.path.join(savepath, "file %s.txt" % row[0]), "wb") as fp:
				urlst = "URL: %s\n\n" % row[1]
				size = "Length: %s\n\n" % row[2]
				fp.write(urlst.encode("utf-8"))
				fp.write(size.encode("utf-8"))
				fp.write("{}".format(row[3]).encode("utf-8"))

def exposed_fix_null():
	'''
	Reset any rows in the table where the `ignoreuntiltime` column
	is null. Updates in 50K row increments.11
	'''
	step = 50000

	with db.session_context() as sess:
		end = sess.execute("""SELECT MAX(id) FROM web_pages WHERE  ignoreuntiltime IS NULL;""")
		end = list(end)[0][0]

		start = sess.execute("""SELECT MIN(id) FROM web_pages WHERE ignoreuntiltime IS NULL;""")
		start = list(start)[0][0]

		changed = 0

		if not start:
			print("No null rows to fix!")
			return

		start = start - (start % step)

		for x in range(start, end, step):
			# SQL String munging! I'm a bad person!
			# Only done because I can't easily find how to make sqlalchemy
			# bind parameters ignore the postgres specific cast
			# The id range forces the query planner to use a much smarter approach which is much more performant for small numbers of updates
			have = sess.execute("""UPDATE web_pages SET ignoreuntiltime = 'epoch'::timestamp WHERE ignoreuntiltime IS NULL AND id < %s AND id >= %s;""" % (x, x-step))
			# print()
			print('%10i, %7.4f, %6i' % (x, x/end * 100, have.rowcount))
			changed += have.rowcount
			if changed > 10000:
				print("Committing (%s changed rows)...." % changed, end=' ')
				sess.commit()
				print("done")
				changed = 0
		sess.commit()


def delete_internal(sess, ids, netloc, badwords):

	if ids:
		print("Updating for netloc(s) %s. %s rows requiring update." % (netloc, len(ids)))
	else:
		print("No rows needing retriggering for netloc %s." % (netloc))

	chunk_size = 2000
	pbar = tqdm.tqdm(range(0, len(ids), chunk_size))
	for chunk_idx in pbar:
		chunk = ids[chunk_idx:chunk_idx+chunk_size]
		while 1:
			try:
				ctbl = version_table(db.WebPages.__table__)

				# Allow ids that only exist in the history table by falling back to a
				# history-table query if the main table doesn't have the ID.
				try:
					ex = sess.query(db.WebPages.url).filter(db.WebPages.id == chunk[0]).one()[0]
				except sqlalchemy.orm.exc.NoResultFound:
					try:
						ex = sess.query(ctbl.c.url).filter(ctbl.c.id == chunk[0]).all()[0][0]
					except IndexError:
						ex = None


				triggered = [tmp for tmp in badwords if ex and tmp in ex]
				pbar.write("Example removed URL: '%s'" % (ex))
				pbar.write("Triggering badwords: '%s'" % triggered)
				if triggered:
					q1 = sess.query(db.WebPages).filter(db.WebPages.id.in_(chunk))
					affected_rows_main = q1.delete(synchronize_session=False)

					q2 = sess.query(ctbl).filter(ctbl.c.id.in_(chunk))
					affected_rows_ver = q2.delete(synchronize_session=False)

					sess.commit()
					pbar.write("Deleted %s rows (%s version table rows) for netloc %s. %0.2f%% done." %
							(affected_rows_main, affected_rows_ver, netloc, 100 * ((chunk_idx) / len(ids))))
				break
			except sqlalchemy.exc.InternalError:
				pbar.write("Transaction error (sqlalchemy.exc.InternalError). Retrying.")
				sess.rollback()
			except sqlalchemy.exc.OperationalError:
				pbar.write("Transaction error (sqlalchemy.exc.OperationalError). Retrying.")
				sess.rollback()
			except sqlalchemy.exc.IntegrityError:
				pbar.write("Transaction error (sqlalchemy.exc.IntegrityError). Retrying.")
				sess.rollback()
			except sqlalchemy.exc.InvalidRequestError:
				pbar.write("Transaction error (sqlalchemy.exc.InvalidRequestError). Retrying.")
				traceback.print_exc()
				sess.rollback()


def exposed_delete_url(netloc, allow_internal=False):
	'''
	Given a netloc, delete all entries for that netloc.

	THIS IS DESTRUCTIVE IN ALL CASES.

	ALL CONTENT is deleted without any filtering.
	'''

	rs = WebMirror.rules.load_rules()

	walked_netlocs = []


	if allow_internal == 'true':
		print("Allow internal is true")
		allow_internal = True
	else:
		print("Allow internal is false")
		allow_internal = False


	for ruleset in rs:
		if ruleset['netlocs']:
			walked_netlocs.extend(ruleset['netlocs'])

	if netloc in walked_netlocs:
		print("WARNING: Netloc %s appears to be still in the walked netlocs list!")
		if not allow_internal:
			raise RuntimeError("Cannot delete walked netloc without allow_internal being 'true'")


	print("Doing delete!")
	bulk_delete_netloc(netloc, main=True, history=False)
	print("Doing history delete!")
	bulk_delete_netloc(netloc, main=False, history=True)


def bulk_delete_netloc(netloc, main=False, history=False):

	commit_interval =  50000
	step            =  10000

	with db.session_context() as sess:
		print("Getting minimum row in need or update..")
		start = sess.execute("""SELECT min(id) FROM web_pages WHERE netloc=:netloc""", {'netloc' : netloc, })
		# start = sess.execute("""SELECT min(id) FROM web_pages WHERE netloc=:netloc OR state = 'specialty_deferred' OR state = 'specialty_ready'""")
		start = list(start)[0][0]
		if start is None:
			print("No rows to reset!")
			return
		print("Minimum row ID:", start, "getting maximum row...")
		stop = sess.execute("""SELECT max(id) FROM web_pages WHERE netloc=:netloc""", {'netloc' : netloc, })
		# stop = sess.execute("""SELECT max(id) FROM web_pages WHERE netloc=:netloc OR state = 'specialty_deferred' OR state = 'specialty_ready'""")
		stop = list(stop)[0][0]
		print("Maximum row ID: ", stop)


		print("Need to fix rows from %s to %s" % (start, stop))
		start = start - (start % step)

		changed = 0
		main_changed = 0
		version_changed = 0
		tot_changed = 0
		pbar = tqdm.tqdm(range(start, stop, step), desc="Deleting")
		for idx in pbar:
			try:
				# SQL String munging! I'm a bad person!
				# Only done because I can't easily find how to make sqlalchemy
				# bind parameters ignore the postgres specific cast
				# The id range forces the query planner to use a much smarter approach which is much more performant for small numbers of updates
				if main:
					have = sess.execute("""DELETE FROM
												web_pages
											WHERE
												netloc = :netloc
											AND
												id > :min_idx
											AND
												id <= :max_idx;""",
												{
													'netloc'  : netloc,
													'min_idx' : idx,
													'max_idx' : idx+step,
												 })
					changed         += have.rowcount
					main_changed    += have.rowcount
					tot_changed     += have.rowcount
				if history:
					have = sess.execute("""DELETE FROM
												web_pages_version
											WHERE
												netloc = :netloc
											AND
												id > :min_idx
											AND
												id <= :max_idx;""",
												{
													'netloc'  : netloc,
													'min_idx' : idx,
													'max_idx' : idx+step,
												 })
					changed         += have.rowcount
					version_changed += have.rowcount
					tot_changed     += have.rowcount

				pbar.set_description("Deleted %s, %s since commit" % (tot_changed, changed))
				# processed  = idx - start
				# total_todo = stop - start
				# print('\r%10i, %10i, %7.4f, %6i, %8i\r' % (idx, stop, processed/total_todo * 100, have.rowcount, tot_changed), end="", flush=True)
				if changed > commit_interval:
					print("Committing (%s changed rows)...." % changed, end=' ')
					sess.commit()
					print("done")
					changed = 0

			except sqlalchemy.exc.OperationalError:
				sess.rollback()
			except sqlalchemy.exc.InvalidRequestError:
				sess.rollback()


		sess.commit()

def exposed_delete_url_history(netloc):
	'''
	Given a netloc, delete all entries in the history table for that netloc.

	THIS IS DESTRUCTIVE IN ALL CASES.

	The history for a URL is deleted without any filtering!
	'''

	print("Delete URL called with netloc param: '%s'" % netloc)
	bulk_delete_netloc(netloc, main=False, history=True)


def exposed_purge_invalid_urls(selected_netloc=None):
	'''
	Iterate over each ruleset in the rules directory, and generate a compound query that will
	delete any matching rows.
	For rulesets with a large number of rows, or many badwords, this
	can be VERY slow.

	Similar in functionality to `clear_bad`, except it results in many fewer queryies,
	and is therefore likely much more performant.
	'''

	print("Purge invalid URLs called with netloc param: '%s'" % selected_netloc)
	found_ruleset = False
	with db.session_context() as sess:
		rs = WebMirror.rules.load_rules()

		random.shuffle(rs)

		for ruleset in rs:

			if      (
							(ruleset['netlocs'] and ruleset['badwords'])
						and
						(
							(ruleset['netlocs'] and ruleset['badwords'] and selected_netloc is None)
							or
							(selected_netloc != None and selected_netloc in ruleset['netlocs'])
						)
					):
				found_ruleset = True
				agg_bad = [tmp for tmp in ruleset['badwords']]
				agg_bad.extend(common.global_constants.GLOBAL_BAD_URLS)

				# So there's no way to escape a LIKE string in postgres.....
				search_strs = ["%{}%".format(badword.replace(r"_", r"\_").replace(r"%", r"\%").replace(r"\\", r"\\")) for badword in agg_bad]

				search_strs.sort()
				print("Netlocs:")
				print(ruleset['netlocs'])
				print("Badwords:")
				for bad in search_strs:
					print("	Bad: ", bad)

				# We have to delete from the normal table before the versioning table,
				# because deleting from the normal table causes inserts into the versioning table
				# due to the change tracking triggers.


				ands = [
						or_(*(db.WebPages.url.like(ss) for ss in search_strs))
					]

				if selected_netloc:
					print("Doing specific netloc filtering!")
					ands.append((db.WebPages.netloc == selected_netloc))
				else:
					print("Filtering by all netlocs in rule file.")
					ands.append(db.WebPages.netloc.in_(ruleset['netlocs']))


				loc = and_(*ands)
				# print("Doing count on table ")
				# count = sess.query(db.WebPages) \
				# 	.filter(or_(*opts)) \
				# 	.count()

				ids = sess.query(db.WebPages.id) \
					.filter(loc)                 \
					.all()

				ids = set(ids)

				if ids == 0:
					print("{num} items match badwords from file {file}. No deletion required ".format(file=ruleset['filename'], num=len(ids)))
				else:
					print("{num} items match badwords from file {file}. Deleting ".format(file=ruleset['filename'], num=len(ids)))


				# Returned list of IDs is each ID packed into a 1-tuple. Unwrap those tuples so it's just a list of integer IDs.
				ids = [tmp[0] for tmp in ids]
				delete_internal(sess, ids, selected_netloc if selected_netloc else ruleset['netlocs'], agg_bad)


	if not found_ruleset:
		print("ERROR!")
		print("Selected netloc (%s) not found in rulesets!" % selected_netloc)

def exposed_purge_invalid_url_history():
	'''
	Functionally identical to `purge_invalid_urls`, but
	operates on the history table only.

	This means that it will operate on row IDs that have been deleted from the main DB (intentionally or not)
	'''

	with db.session_context() as sess:
		ctbl = version_table(db.WebPages.__table__)
		for ruleset in WebMirror.rules.load_rules():

			if ruleset['netlocs'] and ruleset['badwords']:

				agg_bad = [tmp for tmp in ruleset['badwords']]
				agg_bad.extend(common.global_constants.GLOBAL_BAD_URLS)

				# So there's no way to escape a LIKE string in postgres.....
				search_strs = ["%{}%".format(badword.replace(r"_", r"\_").replace(r"%", r"\%").replace(r"\\", r"\\")) for badword in agg_bad]

				print("Badwords:")
				for bad in search_strs:
					print("	Bad: ", bad)
				print("Netlocs:")
				print(ruleset['netlocs'])

				# We have to delete from the normal table before the versioning table,
				# because deleting from the normal table causes inserts into the versioning table
				# due to the change tracking triggers.


				ands = [
						or_(*(ctbl.c.url.like(ss) for ss in search_strs))
					]

				print("Filtering by all netlocs in rule file.")
				ands.append(ctbl.c.netloc.in_(ruleset['netlocs']))


				ids = sess.query(ctbl.c.id) \
					.filter(and_(*ands))                 \
					.all()

				# Collapse duplicates
				ids = set(ids)

				if ids == 0:
					print("{num} items match badwords from file {file}. No deletion required ".format(file=ruleset['filename'], num=len(ids)))
				else:
					print("{num} items match badwords from file {file}. Deleting ".format(file=ruleset['filename'], num=len(ids)))


				# Returned list of IDs is each ID packed into a 1-tuple. Unwrap those tuples so it's just a list of integer IDs.
				ids = [tmp[0] for tmp in ids]
				delete_internal(sess, ids, ruleset['netlocs'], ruleset['badwords'])


def exposed_db_count_netlocs():
	'''
	Select and count the number of instances for each netloc in
	the database.

	Returns the netlocs sorted by count in decending order.
	'''

	with db.session_context() as sess:
		q = sess.query(db.WebPages.netloc, func.count(db.WebPages.netloc).label("count")) \
			.group_by(db.WebPages.netloc)\
			.order_by(desc(func.count(db.WebPages.netloc)))
		print("Doing query.")
		res = q.all()
		res = list(res)
		for row in res:
			print("Row: ", row)

		with open("nl_counts.json", "w") as fp:
			json.dump(res, fp)




def exposed_filter_links(path):
	"""
	Filter a file of urls at `path`. If a url in the file
	is not already a start url in the mirror system, it
	is printed to the console.
	"""
	if not os.path.exists(path):
		raise IOError("File at path '%s' doesn't exist!" % path)

	with open(path, "r") as fp:
		urls = fp.readlines()
	urls = [item.strip() for item in urls if item.strip()]

	# print(urls)

	havestarts = []
	for ruleset in WebMirror.rules.load_rules():
		if ruleset['starturls']:
			havestarts += ruleset['starturls']

	for item in urls:
		if item not in havestarts:
			print(item)


def exposed_fetch_titles(url_file):
	'''
	Fetch a set of urls, and print the page title for each
	'''
	with open(url_file, "r") as fp:
		content = fp.readlines()



	wg = WebRequest.WebGetRobust()

	for url in content:
		url = url.strip()
		meta = common.management.util.get_page_title(wg, url)
		print('Missing: "%s" %s: "%s",' % (url, " " * (50 - len(url)), meta))
		print("('%s',                                                                             '%s',    '%s')," % (meta['title'], url, 'oel' if 'is-orig' in meta and meta['is-orig'] else 'translated'))

	print(content)


def exposed_nu_fetch_sources():
	'''
	Fetch the active sources from NovelUpdates
	'''
	names = WebMirror.SiteSync.fetch.fetch_other_sites()
	for name in names:
		print("	- ", name)



def exposed_find_dead_netlocs():
	'''
	Try to fetch each URL in the available netlocs and see if they're valid.
	'''

	rules = WebMirror.rules.load_rules()
	urls = [item['starturls'] if item['starturls'] else [] + item['feedurls'] if item['feedurls'] else [] for item in rules if not item['rewalk_disabled']]
	urls = [item for sublist in urls for item in sublist]

	urls = list(set([urllib.parse.urlunsplit(urllib.parse.urlsplit(url)[:2] + ("", "", "")) for url in urls]))


	res = {}


	wg = WebRequest.WebGetRobust()
	with ThreadPoolExecutor(max_workers=32) as exc:
		for url in urls:
			res[url] = exc.submit(common.management.util.get_page_title, wg, url)

		for url in urls:
			res[url] = res[url].result()

	with open("bad_urls.json", "w") as fp:
		cont = json.dumps(res, indent=4)
		fp.write(cont)

def exposed_dump_netlocs():
	'''
	Dump the urls to a cache file for comparison purposes.
	'''

	rules = WebMirror.rules.load_rules()
	urls = [item['starturls'] if item['starturls'] else [] for item in rules]
	urls = [item for sublist in urls for item in sublist]
	urls_c = list(set(urls))
	print("Found %s netlocs, %s after filtering for uniqueness." % (len(urls), len(urls_c)))

	with open("url_list.json", "w") as fp:
		cont = json.dumps(urls_c, indent=4)
		fp.write(cont)


def exposed_compare_netlocs():
	'''
	Dump the urls to a cache file for comparison purposes.
	'''
	with open("url_list.json", "r") as fp:
		items = json.load(fp)

	rules = WebMirror.rules.load_rules()
	urls = [item['starturls'] if item['starturls'] else [] for item in rules]
	urls = [item for sublist in urls for item in sublist]
	urls_c = list(set(urls))
	print("Found %s netlocs, %s after filtering for uniqueness." % (len(urls), len(urls_c)))

	for item in items:
		if item not in urls_c:
			print("Missing: %s" % item)



def exposed_process_dead_netlocs():
	'''
	Process the dead-netlocs json file for output
	'''

	with open("bad_urls.json", "r") as fp:
		cont = json.loads(fp.read())

	for item, value in cont.items():
		if 'err' in value:
			value.pop('err')
			print((item, value))


def exposed_count_netlocs():
	'''
	Process the dead-netlocs json file for output
	'''

	rules = WebMirror.rules.load_rules()
	urls = [item['starturls'] if item['starturls'] else [] for item in rules if not item['rewalk_disabled']]
	urls = [item for sublist in urls for item in sublist]

	durls = [item['starturls'] if item['starturls'] else [] for item in rules if item['rewalk_disabled']]
	durls = [item for sublist in durls for item in sublist]

	print("Have %s start urls. %s disabled URLs" % (len(urls), len(durls)))


def _update_feed_name(sess, netloc, oldname, newname):

	have = sess.query(db.RssFeedUrlMapper)            \
		.filter(db.RssFeedUrlMapper.feed_netloc == netloc) \
		.scalar()

	if not have:
		print("Missing: ", have)
		return



	print("Have: ", have, have.feed_entry, have.feed_entry.feed_name)

	if have.feed_entry.feed_name == netloc:
		print("Updating feed name to ", newname)
		have.feed_entry.feed_name = newname
		sess.commit()

def exposed_load_feed_names_from_file(json_file):
	'''
	Given a json file containing a set of 'netloc'->'title' mappings,
	update the feed for each netloc to be 'title'.
	'''

	with open(json_file) as fp:
		df = json.load(fp)


	for url, title in df.items():
		try:
			with db.session_context() as sess:
				fname = WebMirror.OutputFilters.util.feedNameLut.getNiceName(sess, url, debug=True)
				bad = not fname or (fname and fname in url)
				netloc = urllib.parse.urlparse(url).netloc
				if bad:
					_update_feed_name(sess, netloc, netloc, title)
					print((url, title, fname, bad))
		except Exception as e:
			print("Wat?")
			print(e)


def exposed_reset_in_progress():
	'''
	Reset processed downloads that are in progress.
	'''
	WebMirror.UrlUpserter.resetInProgress()

def exposed_unfuck_dropped_feed_name_lut():
	'''
	Remove derp
	'''
	bad_function_content = '''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False
	'''

	with db.session_context() as sess:

		feed_mappers = sess.query(db.RssFeedUrlMapper).order_by(db.RssFeedUrlMapper.id).all()
		netlocs = [tmp.feed_netloc for tmp in feed_mappers]
		assert len(netlocs) == len(set(netlocs))
		feed_mappers = {tmp.feed_netloc : {'id' : tmp.id, 'feed_id' : tmp.feed_id} for tmp in feed_mappers}
		# print(feed_mappers)

		have = sess.query(db.RssFeedEntry).all()
		for item in have:

			urls = [tmp.contenturl for tmp in item.releases if tmp.contenturl]
			netlocs = [urllib.parse.urlparse(url).netloc for url in urls]
			netlocs = list(set(netlocs))

			should_remove = bad_function_content in item.func

			urls = item.urls

			if not should_remove:
				pass
				# for nl in netlocs:
				# 	nls = sess.query(db.RssFeedUrlMapper).filter(db.RssFeedUrlMapper.feed_netloc == nl).all()
				# 	if nls and any([tmp.feed_id != item.id for tmp in nls]):
				# 		print(item.feed_name, [(nl, nl in feed_mappers) for nl in netlocs])
				# 		print("Nls: ", nls)
				# 		nls = sess.query(db.RssFeedUrlMapper)               \
				# 			.filter(db.RssFeedUrlMapper.feed_netloc == nl)  \
				# 			.filter(db.RssFeedUrlMapper.feed_id != item.id) \
				# 			.update({'feed_id': item.id})

				# 	elif nl in feed_mappers:
				# 		pass
				# 	else:
				# 		print(item.feed_name, [(nl, nl in feed_mappers) for nl in netlocs])
				# 		print("Needs to add:", nl)
				# 		new = db.RssFeedUrlMapper(
				# 				feed_netloc = nl,
				# 				feed_id     = item.id,
				# 			)
				# 		sess.add(new)

				# sess.commit()
			else:
				if item.feed_name.endswith(".com") or item.feed_name.endswith(".net") or item.feed_name.endswith(".org"):
					if not urls:
						print("Should delete:", item.feed_name, item, should_remove, urls)
						for rel in item.releases:
							sess.delete(rel)
						sess.delete(item)
						sess.commit()
				else:

					print("Unknown delete:", item.feed_name, item, should_remove, urls)




def exposed_fetch_other_feed_sources():
	'''
	Walk the listed pages for both AhoUpdates and NovelUpdates,
	retrieving a list of the translators from each.
	'''
	WebMirror.SiteSync.fetch.fetch_other_sites()


def exposed_fix_missing_history():
	'''
	Fix any items that don't have an entry in the history table.
	'''
	Misc.HistoryAggregator.Consolidate.fix_missing_history()

def exposed_truncate_transaction_table():
	'''
	Truncate the db versioning table.
	'''
	trunc = Misc.HistoryAggregator.Consolidate.TransactionTruncator()
	print("Truncator: ", trunc)
	trunc.truncate_transaction_table()


def exposed_flatten_history():
	'''
	Flatten the page change history.
	This limits the retained page versions to one-per-hour for the
	last 48 hours, once per day for the last 32 days, and once per
	week after that.
	'''
	Misc.HistoryAggregator.Consolidate.consolidate_history()

def exposed_flatten_fix_missing_history():
	'''
	Functionally equivalent to `flatten_history`, `fix_missing_history`
	'''
	Misc.HistoryAggregator.Consolidate.consolidate_history()
	Misc.HistoryAggregator.Consolidate.fix_missing_history()


def exposed_test_new_job_queue():
	'''
	Testing function for JobDispatcher components
	'''

	instance = WebMirror.JobDispatcher.JobAggregatorInternal(None, None)

	want = instance.outbound_job_wanted("www.novelupdates.com", "http://www.novelupdates.com/")
	print(want)
	want = instance.outbound_job_wanted("twitter.com", "https://twitter.com/Baka_Tsuki")
	print(want)
	want = instance.outbound_job_wanted("twitter.com", "https://twitter.com/Nano_Desu_Yo")
	print(want)


def exposed_delete_error_versions():
	'''
	Reset the priority of every row in the table to the IDLE_PRIORITY level
	'''

	step   = 10000
	commit = 10000

	with db.session_context() as sess:
		try:
			sess.execute("SET statement_timeout TO 0;")


			print("Getting minimum row in need or update..")
			start = sess.execute("""SELECT min(id) FROM web_pages_version WHERE  (state = 'error' OR state = 'fetching')""")
			start = list(start)[0][0]
			if start is None:
				print("No rows to reset!")
				return
			print("Minimum row ID: ", start, "getting maximum row...")
			stop = sess.execute("""SELECT max(id) FROM web_pages_version WHERE  (state = 'error' OR state = 'fetching')""")
			stop = list(stop)[0][0]
			print("Maximum row ID: ", stop)


			print("Need to fix rows from %s to %s" % (start, stop))
			start = start - (start % step)

			changed = 0
			changed_tot = 0
			pb = tqdm.tqdm(range(stop, start, step*-1), desc='Clearing error states.')
			for idx in pb:
				try:
					# SQL String munging! I'm a bad person!
					# Only done because I can't easily find how to make sqlalchemy
					# bind parameters ignore the postgres specific cast
					# The id range forces the query planner to use a much smarter approach which is much more performant for small numbers of updates
					have = sess.execute("""DELETE FROM web_pages_version WHERE (state = 'error' OR state = 'fetching') AND id > {} AND id <= {};""".format(idx, idx+step))
					# print()

					# processed  = idx - start
					# total_todo = stop - start
					desc = '%6i, %6i, %6i' % (have.rowcount, changed, changed_tot)
					pb.set_description(desc)

					# print('\r%10i, %10i, %7.4f, %6i, %6i, %6i\r' % (idx, stop, processed/total_todo * 100, have.rowcount, changed, changed_tot), end="", flush=True)
					changed += have.rowcount
					changed_tot += have.rowcount
					if changed > commit:
						print("Committing (%s changed rows)...." % changed, end=' ')
						sess.commit()
						print("done")
						changed = 0

				except sqlalchemy.exc.OperationalError:
					sess.rollback()
				except sqlalchemy.exc.InvalidRequestError:
					sess.rollback()


			sess.commit()
		finally:
			sess.execute("RESET statement_timeout;")

def exposed_block_special_case_netlocs():
	'''
	Reset the priority of every row in the table to the IDLE_PRIORITY level
	'''

	step   = 50000
	commit = 10000

	with db.session_context() as sess:
		print("Getting minimum row in need or update..")
		start = sess.execute("""SELECT min(id) FROM web_pages WHERE state != 'specialty_blocked' AND netloc IN :nl_set""", { 'nl_set' : ('storiesonline.net', ) })
		start = list(start)[0][0]
		if start is None:
			print("No rows to reset!")
			return
		print("Minimum row ID: ", start, "getting maximum row...")
		stop = sess.execute("""SELECT max(id) FROM web_pages WHERE state != 'specialty_blocked' AND netloc IN :nl_set""", { 'nl_set' : ('storiesonline.net', ) })
		stop = list(stop)[0][0]
		print("Maximum row ID: ", stop)


		print("Need to fix rows from %s to %s" % (start, stop))
		start = start - (start % step)

		changed = 0
		changed_tot = 0
		pb = tqdm.tqdm(range(stop, start, step*-1), desc='Clearing error states.')
		for idx in pb:
			try:
				# SQL String munging! I'm a bad person!
				# Only done because I can't easily find how to make sqlalchemy
				# bind parameters ignore the postgres specific cast
				# The id range forces the query planner to use a much smarter approach which is much more performant for small numbers of updates
				have = sess.execute("""UPDATE web_pages SET state='specialty_blocked' WHERE netloc IN :nl_set AND id > :id_min AND id <= :id_max;""",
					{'nl_set' : ('storiesonline.net', ), 'id_min' : idx, 'id_max' : idx+step}
					)
				# print()

				# processed  = idx - start
				# total_todo = stop - start
				desc = '%6i, %6i, %6i' % (have.rowcount, changed, changed_tot)
				pb.set_description(desc)

				# print('\r%10i, %10i, %7.4f, %6i, %6i, %6i\r' % (idx, stop, processed/total_todo * 100, have.rowcount, changed, changed_tot), end="", flush=True)
				changed += have.rowcount
				changed_tot += have.rowcount
				if changed > commit:
					print("Committing (%s changed rows)...." % changed, end=' ')
					sess.commit()
					print("done")
					changed = 0

			except sqlalchemy.exc.OperationalError:
				sess.rollback()
			except sqlalchemy.exc.InvalidRequestError:
				sess.rollback()


		sess.commit()

def exposed_drop_priorities():
	'''
	Reset the priority of every row in the table to the IDLE_PRIORITY level
	'''

	step  = 50000

	with db.session_context(override_timeout_ms=30*60*1000) as sess:
		print("Getting minimum row in need or update..")
		start = sess.execute("""SELECT min(id) FROM web_pages WHERE priority != 9""")
		start = list(start)[0][0]
		if start is None:
			print("No rows to reset!")
			return
		print("Minimum row ID: ", start, "getting maximum row...")
		stop = sess.execute("""SELECT max(id) FROM web_pages WHERE priority != 9""")
		stop = list(stop)[0][0]
		print("Maximum row ID: ", stop)

		if not start:
			print("No null rows to fix!")
			return

		print("Need to fix rows from %s to %s" % (start, stop))
		start = start - (start % step)

		changed = 0
		changed_tot = 0
		pb = tqdm.tqdm(range(start, stop, step), desc='Dropping priorities.')
		for idx in pb:
			try:
				# SQL String munging! I'm a bad person!
				# Only done because I can't easily find how to make sqlalchemy
				# bind parameters ignore the postgres specific cast
				# The id range forces the query planner to use a much smarter approach which is much more performant for small numbers of updates
				have = sess.execute("""update web_pages set priority = 9 where priority != 9 AND id > {} AND id <= {};""".format(idx, idx+step))
				# print()

				# processed  = idx - start
				# total_todo = stop - start
				desc = '%6i, %6i, %6i' % (have.rowcount, changed, changed_tot)
				pb.set_description(desc)

				# print('\r%10i, %10i, %7.4f, %6i, %6i, %6i\r' % (idx, stop, processed/total_todo * 100, have.rowcount, changed, changed_tot), end="", flush=True)
				changed += have.rowcount
				changed_tot += have.rowcount
				if changed > step:
					print("Committing (%s changed rows)...." % changed, end=' ')
					sess.commit()
					print("done")
					changed = 0

			except sqlalchemy.exc.OperationalError:
				sess.rollback()
			except sqlalchemy.exc.InvalidRequestError:
				sess.rollback()


		sess.commit()


def unwrap_ret(ret):

	ret = list(ret)
	if not ret:
		print("Not list ret!", list(ret))
		return 0

	if not ret[0]:
		print("Not ret[0]", ret[0])
		return 0
	if not ret[0][0]:
		print("Coercing to zero?")
		return 0
	print("Returning ret[0][0]: ", ret[0][0])
	return ret[0][0]

def delete_by_netloc_internal(netloc):
	'''
	List netlocs from database that aren't in the rules.
	'''

	step  = 10000

	with db.session_context() as sess:
		print("Getting minimum row in need or update..")
		start = sess.execute("""SELECT min(id) FROM web_pages WHERE netloc = :nl""", {"nl":netloc})
		start = unwrap_ret(start)
		print("Minimum row ID: ", start, "getting maximum row...")
		stop = sess.execute("""SELECT max(id) FROM web_pages WHERE netloc = :nl""", {"nl":netloc})
		stop = unwrap_ret(stop)
		print("Maximum row ID: ", stop)

		startv = sess.execute("""SELECT min(id) FROM web_pages_version WHERE netloc = :nl""", {"nl":netloc})
		startv = unwrap_ret(startv)
		print("Minimum version row ID: ", startv, "getting maximum version row...")
		stopv = sess.execute("""SELECT max(id) FROM web_pages_version WHERE netloc = :nl""", {"nl":netloc})
		stopv = unwrap_ret(stopv)
		print("Maximum version row ID: ", stopv)

		if not (start or startv) :
			print("No null rows to fix!")
			return

		print("Need to fix rows from %s to %s" % (start, stop))
		print("Need to fix version rows from %s to %s" % (startv, stopv))
		start = start - (start % step)

		changed = 0
		for idx in range(start, stop, step):
			try:
				# SQL String munging! I'm a bad person!
				# Only done because I can't easily find how to make sqlalchemy
				# bind parameters ignore the postgres specific cast
				# The id range forces the query planner to use a much smarter approach which is much more performant for small numbers of updates
				have = sess.execute("""DELETE FROM web_pages WHERE netloc = :nl AND id > :idmin AND id <= :idmax;""", {'idmin':idx, 'idmax':idx+step, 'nl':netloc})
				# print()

				processed  = idx - start
				total_todo = stop - start
				print('%10i, %10i, %7.4f, %6i' % (idx, stop, processed/total_todo * 100, have.rowcount))
				changed += have.rowcount
				if changed > step:
					print("Committing (%s changed rows)...." % changed, end=' ')
					sess.commit()
					print("done")
					changed = 0

			except sqlalchemy.exc.OperationalError:
				sess.rollback()
			except sqlalchemy.exc.InvalidRequestError:
				sess.rollback()


		changed = 0
		for idx in range(startv, stopv, step):
			try:
				# SQL String munging! I'm a bad person!
				# Only done because I can't easily find how to make sqlalchemy
				# bind parameters ignore the postgres specific cast
				# The id range forces the query planner to use a much smarter approach which is much more performant for small numbers of updates
				have = sess.execute("""DELETE FROM web_pages_version WHERE netloc = :nl AND id > :idmin AND id <= :idmax;""", {'idmin':max(idx-1, 0), 'idmax':idx+step+1, 'nl':netloc})
				# print()

				processed  = idx - startv
				total_todo = stopv - startv
				print('%10i, %10i, %7.4f, %6i' % (idx, stopv, processed/total_todo * 100, have.rowcount))
				changed += have.rowcount
				if changed > step:
					print("Committing (%s changed rows)...." % changed, end=' ')
					sess.commit()
					print("done")
					changed = 0

			except sqlalchemy.exc.OperationalError:
				sess.rollback()
			except sqlalchemy.exc.InvalidRequestError:
				sess.rollback()

		sess.commit()

def exposed_delete_transactions():
	'''
	List netlocs from database that aren't in the rules.
	'''

	with db.session_context() as sess:

		print("Getting minimum transaction table date..")
		start = sess.execute("""SELECT min(issued_at) FROM transaction""")
		start = unwrap_ret(start)
		print("Minimum transaction time: ", start, "getting maximum transaction table date...")
		stop = sess.execute("""SELECT max(issued_at) FROM transaction""")
		stop = unwrap_ret(stop)
		print("Maximum transaction time: ", stop)

		step = datetime.timedelta(hours=8)
		mind = start
		while mind < stop:
			print("Doing delete from %s to %s" % (mind, mind+step))

			have = sess.execute("""DELETE FROM transaction WHERE issued_at >= :startd AND issued_at <= :stopd;""", {'startd':mind, 'stopd':mind+step})
			print('Deleted %6i rows. Committing...' % (have.rowcount, ))
			sess.commit()
			print('Comitted')


			mind += step


def exposed_delete_netlocs():
	'''
	List netlocs from database that aren't in the rules.
	'''
	rm = [
		'www.wattpad.com',                                                                                     # - [(2,)]
		'www.booksie.com',                                                                                     # - [(4369566,)]
	]


	with db.session_context() as sess:
		print("Doing web_pages delete")
		have = sess.execute("""DELETE FROM web_pages WHERE netloc = 'www.wattpad.com' OR netloc = 'www.booksie.com';""")
		print("Deleted %s rows. committing" % have.rowcount)
		sess.commit()
		print("Doing web_pages_version delete")
		have = sess.execute("""DELETE FROM web_pages_version WHERE netloc = 'www.wattpad.com' OR netloc = 'www.booksie.com';""")
		print("Deleted %s rows. committing" % have.rowcount)
		sess.commit()
		print("Done!")



def exposed_rolling_rewalk():

	run = WebMirror.TimedTriggers.RollingRewalkTriggers.RollingRewalkTriggersBase()
	run._go()


def exposed_rewalk_all_old():

	run = WebMirror.TimedTriggers.RollingRewalkTriggers.RollingRewalkTriggersBase()
	run.retrigger_other()





def exposed_nu_retrigger_series_pages():
	'''

	'''
	step = 500000

	with db.session_context() as sess:
		end = sess.execute("""SELECT MAX(id) FROM web_pages;""")
		end = list(end)[0][0]

		start = sess.execute("""SELECT MIN(id) FROM web_pages;""")
		start = list(start)[0][0]

		changed = 0

		if not start:
			print("No null rows to fix!")
			return

		start = start - (start % step)

		for x in range(start, end, step):

			have = sess.execute("""UPDATE web_pages SET state='new', priority=50000 WHERE url LIKE 'http://www.novelupdates.com/series/%%/' AND id < %s AND id >= %s AND state != 'new';""" % (x, x-step))

			print('%10i, %7.4f, %6i, %6i' % (x, x/end * 100, have.rowcount, changed))
			changed += have.rowcount
			if changed > 100:
				print("Committing (%s changed rows)...." % changed, end=' ')
				sess.commit()
				print("done")
				changed = 0
		sess.commit()




def get_wln_release_urls():
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

def filter_get_have_url(netloc_dict, fetch_title):


	rules = WebMirror.rules.load_rules()
	urls = [item['starturls'] if item['starturls'] else [] + item['feedurls'] if item['feedurls'] else [] for item in rules]
	urls = [item for sublist in urls for item in sublist]

	starturldict = {}

	for url in urls:
		itemnl = WebMirror.OutputFilters.util.feedNameLut.patch_blogspot(urllib.parse.urlsplit(url).netloc)
		starturldict.setdefault(itemnl, [])
		starturldict[itemnl] = url

	wg = WebRequest.WebGetRobust()


	missing = 0

	with db.session_context() as sess:
		for netloc, tgturl_set in netloc_dict.items():

			if not netloc:
				continue
			if netloc in common.global_constants.NU_NEW_MASK_NETLOCS:
				continue
			if any([tmp in netloc for tmp in common.global_constants.GLOBAL_BAD_URLS]):
				continue

			if any([
						badstr in tmp
					for
						badstr in common.global_constants.GLOBAL_BAD_URLS
					for
						tmp in tgturl_set
					]):
				continue

			if netloc.startswith("http://www.novelupdates.com/") or netloc.startswith("https://www.novelupdates.com/"):
				continue

			if WebMirror.OutputFilters.util.feedNameLut.getNiceName(sess, srcurl=None, netloc=netloc):
				continue

			if netloc in starturldict:
				continue

			random_nl = next(iter(tgturl_set))
			title = netloc
			if fetch_title:
				title = common.management.util.get_page_title(wg, random_nl)
			print("Missing: ", (netloc, title, random_nl))
			missing += 1

	print("Total outbound items: ", len(netloc_dict), "missing:", missing)

def exposed_new_from_wln_feeds(fetch_title=False):
	'''
	Parse the local WLN instance's release listing and extract the found release urls
	that are not in the known feednamelut.
	'''
	nlfilter = get_wln_release_urls()
	filter_get_have_url(nlfilter, fetch_title)


def exposed_new_from_nu_feeds(fetch_title=False):
	'''
	Parse outbound netlocs from NovelUpdates releases, extracting
	any sites that are not known in the feednamelut.
	'''

	mapdict = get_nu_head_urls()
	filter_get_have_url(mapdict, fetch_title)

def exposed_new_from_all_feeds(fetch_title=False):
	'''
	Parse outbound netlocs from NovelUpdates and WLN releases, extracting
	any sites that are not known in the feednamelut.
	'''

	nlfilter = get_wln_release_urls()
	mapdict = get_nu_head_urls()

	print("NU Header urls: %s, wln URLs: %s" % (len(mapdict), len(nlfilter)))

	for key, value in nlfilter.items():
		mapdict.setdefault(key, set())
		mapdict[key].update(value)

	filter_get_have_url(mapdict, fetch_title)


def exposed_purge_squatter_content():


	proc = WebMirror.processor.HtmlProcessor.HtmlPageProcessor(
			baseUrls        = None,
			pageUrl         = None,
			pgContent       = True,
			loggerPath      = None,
			relinkable      = None,
			stripTitle      = None,
			destyle         = None,
			preserveAttrs   = None,
			decompose_svg   = None,

			decompose       = [],
			decomposeBefore = [],

		)

	engine = WebMirror.Engine.SiteArchiver(None, None, None)

	with db.session_context() as sess:
		print("Querying for count")
		count = sess.query(db.WebPages.id).count()
		print("Tital count")
		print("Querying for rows")
		iterable = sess.query(db.WebPages.id, db.WebPages.url, db.WebPages.netloc, db.WebPages.content) \
			.order_by(db.WebPages.netloc)                                          \
			.yield_per(1000)
		rows = 0
		skipped = []



		for rid, url, netloc, content in tqdm.tqdm(iterable, total=count):
			try:
				if content:
					proc.checkSquatters(content)
			except GarbageDomainSquatterException:
				print("Squatter page: ", url)
				skipped.append((rid, url, netloc))

	with open("dump.json", "w") as fp:
		json.dump(skipped, fp)
