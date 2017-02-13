
import calendar
import datetime
import json
import os
import os.path
import shutil
import traceback
from concurrent.futures import ThreadPoolExecutor

import urllib.error
import urllib.parse

from sqlalchemy import and_
from sqlalchemy import or_
import sqlalchemy.exc
from sqlalchemy_continuum.utils import version_table

if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()

from WebMirror.Engine import SiteArchiver
import WebMirror.OutputFilters.util.feedNameLut as feedNameLut
import WebMirror.rules
import WebMirror.SiteSync.fetch
import WebMirror.SpecialCase
import WebMirror.NewJobQueue

import RawArchiver.RawActiveModules
import RawArchiver.RawEngine

import common.database as db
import common.Exceptions
import common.management.file_cleanup

import Misc.HistoryAggregator.Consolidate

import flags
import config
from config import C_RAW_RESOURCE_DIR

import WebMirror.TimedTriggers.QueueTriggers
import WebMirror.OutputFilters.rss.FeedDataParser

def exposed_remote_fetch_enqueue(url):
	'''
	Place a normal fetch request for url `url` into the remote fetch queue.

	Requires the FetchAgent service to be running.
	'''

	print("Enqueueing ")
	trig = WebMirror.TimedTriggers.QueueTriggers.NuQueueTrigger()
	trig.enqueue_url(url)

def exposed_trigger_nu_homepage_fetch():
	'''
	Trigger testing for the QueueTrigger system
	'''
	trig = WebMirror.TimedTriggers.QueueTriggers.NuQueueTrigger()
	trig.go()


def exposed_fetch(url, debug=True, rss_debug=False):
	'''
	Do a synchronous fetch of content from url `url`.
	'''

	# try:
	# 	WebMirror.SpecialCase.startAmqpFetcher()
	# except RuntimeError:  # Fetcher already started
	# 	pass

	if rss_debug:
		print("Debugging RSS")
		flags.RSS_DEBUG = True

	parsed = urllib.parse.urlparse(url)
	root = urllib.parse.urlunparse((parsed[0], parsed[1], "", "", "", ""))

	new = db.WebPages(
		url       = url,
		starturl  = root,
		netloc    = parsed.netloc,
		distance  = 50000,
		is_text   = True,
		priority  = 500000,
		type      = 'unknown',
		fetchtime = datetime.datetime.now(),
		)

	if debug:
		print(new)

	try:
		archiver = SiteArchiver(None, db.get_db_session(), None)
		job     = archiver.synchronousJobRequest(url, ignore_cache=True)
	except Exception as e:
		traceback.print_exc()
	finally:
		db.delete_db_session()

def exposed_fetch_silent(tgt):
	'''
	Identical to `test_retrieve`, except debug printing is supressed.
	'''
	exposed_fetch(tgt, debug=False)

def exposed_fetch_rss(tgt):
	'''
	Identical to `test_retrieve`, except debug printing is supressed and RSS debugging is enabled.
	'''
	exposed_fetch(tgt, debug=False, rss_debug=True)

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


	sess = db.get_db_session()

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
		job     = archiver.do_job(row)
	except Exception as e:
		traceback.print_exc()
	finally:
		db.delete_db_session()

def exposed_test_head(url, referrer):
	'''
	Do a HTTP HEAD for url `url`, passing the referrer `referrer`.
	'''

	try:
		WebMirror.SpecialCase.startAmqpFetcher()
	except RuntimeError:  # Fetcher already started
		pass

	try:
		WebMirror.SpecialCase.blockingRemoteHead(url, referrer)
	except Exception as e:
		traceback.print_exc()
	finally:
		WebMirror.SpecialCase.stopAmqpFetcher()

	print("exposed_test_head complete!")

def exposed_test_all_rss():
	'''
	Fetch all RSS feeds and process each. Done with 8 parallel workers.
	'''
	print("fetching and debugging RSS feeds")
	rules = WebMirror.rules.load_rules()
	feeds = [item['feedurls'] for item in rules]
	feeds = [item for sublist in feeds for item in sublist]

	flags.RSS_DEBUG = True
	with ThreadPoolExecutor(max_workers=8) as executor:
		for url in feeds:
			try:
				executor.submit(exposed_fetch, url, debug=False)
			except common.Exceptions.DownloadException:
				print("failure downloading page!")
			except urllib.error.URLError:
				print("failure downloading page!")

def exposed_longest_rows():
	'''
	Fetch the rows from the database where the `content` field is longest.
	Return is limited to the biggest 50 rows.
	VERY SLOW (has to scan the entire table)
	'''
	print("Getting longest rows from database")
	have = db.get_db_session().execute("""
		SELECT
			id, url, length(content), content
		FROM
			web_pages
		ORDER BY
			LENGTH(content) DESC NULLS LAST
		LIMIT 50;
		""")
	print("Rows:")

	import os
	import os.path

	savepath = "./large_files/"
	for row in have:
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


	end = db.get_db_session().execute("""SELECT MAX(id) FROM web_pages WHERE  ignoreuntiltime IS NULL;""")
	end = list(end)[0][0]

	start = db.get_db_session().execute("""SELECT MIN(id) FROM web_pages WHERE ignoreuntiltime IS NULL;""")
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
		have = db.get_db_session().execute("""UPDATE web_pages SET ignoreuntiltime = 'epoch'::timestamp WHERE ignoreuntiltime IS NULL AND id < %s AND id >= %s;""" % (x, x-step))
		# print()
		print('%10i, %7.4f, %6i' % (x, x/end * 100, have.rowcount))
		changed += have.rowcount
		if changed > 10000:
			print("Committing (%s changed rows)...." % changed, end=' ')
			db.get_db_session().commit()
			print("done")
			changed = 0
	db.get_db_session().commit()

def exposed_delete_comment_feed_items():
	'''
	Iterate over all retreived feed article entries, and delete any that look
	like they're comment feed articles.
	'''
	sess = db.get_db_session()
	bad = sess.query(db.FeedItems) \
			.filter(or_(
				db.FeedItems.contenturl.like("%#comment-%"),
				db.FeedItems.contenturl.like("%CommentsForInMyDaydreams%"),
				db.FeedItems.contenturl.like("%www.fanfiction.net%"),
				db.FeedItems.contenturl.like("%www.fictionpress.com%"),
				db.FeedItems.contenturl.like("%www.booksie.com%")))    \
			.order_by(db.FeedItems.contenturl) \
			.all()

	count = 0
	for bad in bad:
		print(bad.contenturl)

		while bad.author:
			bad.author.pop()
		while bad.tags:
			bad.tags.pop()
		sess.delete(bad)
		count += 1
		if count % 1000 == 0:
			print("Committing at %s" % count)
			sess.commit()

	print("Done. Committing...")
	sess.commit()

def exposed_update_feed_names():
	'''
	Apply any new feednamelut names to existing fetched RSS posts.
	'''
	for key, value in feedNameLut.mapper.items():
		feed_items = db.get_db_session().query(db.FeedItems) \
				.filter(db.FeedItems.srcname == key)    \
				.all()
		if feed_items:
			for item in feed_items:
				item.srcname = value
			print(len(feed_items))
			print(key, value)
			db.get_db_session().commit()

def exposed_clear_bad():
	'''
	Iterate over all blocked strings from the various YAML rules,
	deleting any occurances of each from the database.
	SLOW
	'''
	from sqlalchemy.dialects import postgresql

	rules = WebMirror.rules.load_rules()

	for ruleset in rules:

		print("Cleaning ruleset")
		# print(ruleset['netlocs'])
		# print(ruleset.keys())
		for badword in ruleset['badwords']:
			if not ruleset['netlocs']:
				continue
			if "%" in badword:
				print(badword)
			else:
				print("Deleting items containing string: '%s'" % badword)
				q = db.get_db_session().query(db.WebPages)                   \
					.filter(db.WebPages.netloc.in_(ruleset['netlocs']))   \
					.filter(db.WebPages.url.like("%{}%".format(badword)))
				items = q.count()
				if items:
					print("%s results for : '%s'" % (items, badword))

					q = db.get_db_session().query(db.WebPages)                   \
						.filter(db.WebPages.netloc.in_(ruleset['netlocs']))   \
						.filter(db.WebPages.url.like("%{}%".format(badword))) \
						.delete(synchronize_session=False)
					db.get_db_session().commit()

def exposed_purge_invalid_urls(selected_netloc=None):
	'''
	Iterate over each ruleset in the rules directory, and generate a compound query that will
	delete any matching rows.
	For rulesets with a large number of rows, or many badwords, this
	can be VERY slow.

	Similar in functionality to `clear_bad`, except it results in many fewer queryies,
	and is therefore likely much more performant.
	'''

	sess = db.get_db_session()
	for ruleset in WebMirror.rules.load_rules():

		if      (
						(ruleset['netlocs'] and ruleset['badwords'])
					and
					(
						(ruleset['netlocs'] and ruleset['badwords'] and selected_netloc is None)
						or
						(selected_netloc != None and selected_netloc in ruleset['netlocs'])
					)
				):
			# We have to delete from the normal table before the versioning table,
			# because deleting from the normal table causes inserts into the versioning table
			# due to the change tracking triggers.

			count = 1
			ands = [
					or_(*(db.WebPages.url.like("%{}%".format(badword)) for badword in ruleset['badwords']))
				]

			if selected_netloc:
				ands.append((db.WebPages.netloc == selected_netloc))
			else:
				ands.append(db.WebPages.netloc.in_(ruleset['netlocs']))


			loc = and_(*ands)
			# print("Doing count on table ")
			# count = sess.query(db.WebPages) \
			# 	.filter(or_(*opts)) \
			# 	.count()

			if selected_netloc:
				print(loc)

			if count == 0:
				print("{num} items match badwords from file {file}. No deletion required ".format(file=ruleset['filename'], num=count))
			else:
				print("{num} items match badwords from file {file}. Deleting ".format(file=ruleset['filename'], num=count))

				sess.query(db.WebPages) \
					.filter(or_(*loc)) \
					.delete(synchronize_session=False)


			# # Do the delete from the versioning table now.
			ctbl = version_table(db.WebPages)
			loc2 = and_(
					ctbl.c.netloc.in_(ruleset['netlocs']),
					or_(*(ctbl.c.url.like("%{}%".format(badword)) for badword in ruleset['badwords']))
				)
			# print("Doing count on Versioning table ")
			# count = sess.query(ctbl) \
			# 	.filter(or_(*opts)) \
			# 	.count()

			if count == 0:
				print("{num} items in versioning table match badwords from file {file}. No deletion required ".format(file=ruleset['filename'], num=count))
			else:
				print("{num} items in versioning table match badwords from file {file}. Deleting ".format(file=ruleset['filename'], num=count))

				sess.query(ctbl) \
					.filter(or_(*loc2)) \
					.delete(synchronize_session=False)



			sess.commit()


		# print(ruleset['netlocs'])
		# print(ruleset['badwords'])

def exposed_sort_json(json_name):
	'''
	Load a file of feed missed json entries, and sort it into
	a much nicer to read output format.

	Used internally by the rss_db/rss_day/week/month functionality.
	'''
	with open(json_name) as fp:
		cont = fp.readlines()
	print("Json file has %s lines." % len(cont))

	data = {}
	for line in cont:
		val = json.loads(line)
		name = val['SourceName']
		if not name in data:
			data[name] = []

		data[name].append(val)
	out = []
	for key in data:

		out.append((data[key][0]['Have Func'], len(data[key]), data[key]))

	out.sort(key=lambda x: (x[0], x[1]*-1))
	out.sort(key=lambda x: (x[1]*-1))

	key_order = [
		"Have Func",
		"SourceName",
		"Title",
		"Tags",
		"Feed URL",
		"Vol",
		"Chp",
		"Frag",
		"Postfix",
		"GUID",
	]

	outf = json_name+".pyout"
	try:
		os.unlink(outf)
	except FileNotFoundError:
		pass

	with open(outf, "w") as fp:
		for item in out:
			# print(item[1])
			items = item[2]
			[tmp['Tags'].sort() for tmp in items]
			items.sort(key=lambda x: (x['Tags'], x['Title']))

			for value in items:
				for key in key_order:
					fp.write("%s, " % ((key, value[key]), ))
				fp.write("\n")

def exposed_rss_db_sync(target = None, days=False, silent=False):
	'''
	Feed RSS feed history through the feedparsing system, generating a log
	file of the feed articles that were not captured by the feed parsing system.

	Target is an optional netloc. If not none, only feeds with that netloc are
		processed.
	Days is the number of days into the past to process. None results in all
		available history being read.
	Silent suppresses some debug printing to the console.
	'''

	json_file = 'rss_filter_misses-1.json'

	write_debug = True
	if silent:
		config.C_DO_RABBIT = False
	if target:
		config.C_DO_RABBIT = False
		flags.RSS_DEBUG    = True
		write_debug = False
	else:
		try:
			os.unlink(json_file)
		except FileNotFoundError:
			pass

	import WebMirror.processor.RssProcessor
	parser = WebMirror.processor.RssProcessor.RssProcessor(loggerPath   = "Main.RssDb",
															pageUrl     = 'http://www.example.org',
															pgContent   = '',
															type        = 'application/atom+xml',
															transfer    = False,
															debug_print = True,
															db_sess = None,
															write_debug = write_debug)


	print("Getting feed items....")

	if target:
		print("Limiting to '%s' source." % target)
		feed_items = db.get_db_session().query(db.FeedItems) \
				.filter(db.FeedItems.srcname == target)    \
				.order_by(db.FeedItems.srcname)           \
				.order_by(db.FeedItems.title)           \
				.all()
	elif days:
		print("RSS age override: ", days)
		cutoff = datetime.datetime.now() - datetime.timedelta(days=days)
		feed_items = db.get_db_session().query(db.FeedItems) \
				.filter(db.FeedItems.published > cutoff)  \
				.order_by(db.FeedItems.srcname)           \
				.order_by(db.FeedItems.title)             \
				.all()
	else:
		feed_items = db.get_db_session().query(db.FeedItems) \
				.order_by(db.FeedItems.srcname)           \
				.order_by(db.FeedItems.title)           \
				.all()


	print("Feed items: ", len(feed_items))

	for item in feed_items:
		ctnt = {}
		ctnt['srcname']   = item.srcname
		ctnt['title']     = item.title
		ctnt['tags']      = item.tags
		ctnt['linkUrl']   = item.contenturl
		ctnt['guid']      = item.contentid
		ctnt['published'] = calendar.timegm(item.published.timetuple())

		# Pop()ed off in processFeedData().
		ctnt['contents']  = 'wat'

		try:
			parser.processFeedData(ctnt, tx_raw=False, tx_parse=not bool(days))
		except ValueError:
			pass
		# print(ctnt)
	if target == None:
		exposed_sort_json(json_file)

def exposed_rss_db_silent():
	'''
	Eqivalent to rss_db_sync(None, False, True)
	'''
	exposed_rss_db_sync(silent=True)

def exposed_rss_day():
	'''
	Eqivalent to rss_db_sync(1)

	Effectively just processes the last day of feed entries.
	'''
	exposed_rss_db_sync(days=1)

def exposed_rss_week():
	'''
	Eqivalent to rss_db_sync(7)

	Effectively just processes the last week of feed entries.
	'''
	exposed_rss_db_sync(days=7)

def exposed_rss_month():
	'''
	Eqivalent to rss_db_sync(45)

	Effectively just processes the last 45 days of feed entries.
	'''
	exposed_rss_db_sync(days=45)


def exposed_rss_missing_functions():
	'''
	Print skeleton functions for the RSS source names that are
	not present in the lookup map.
	'''
	WebMirror.OutputFilters.rss.FeedDataParser.print_missing_functions()

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

def get_page_title(wg, url):
	chunks = url.split("/")
	baseurl = "/".join(chunks[:3])
	title = urllib.parse.urlsplit(url).netloc

	try:
		soup = wg.getSoup(baseurl)
		if soup.title:
			title = soup.title.get_text().strip()
	except Exception:
		pass

	return title

def exposed_missing_lut(fetchTitle=False):
	'''
	Iterate over distinct RSS feed sources in database,
	and print any for which there is not an entry in
	feedDataLut.py to the console.
	'''
	import WebMirror.OutputFilters.util.feedNameLut as fnl
	import common.util.webFunctions as webFunctions
	wg = webFunctions.WebGetRobust()
	rules = WebMirror.rules.load_rules()
	feeds = [item['feedurls'] for item in rules]
	feeds = [item for sublist in feeds for item in sublist]
	# feeds = [urllib.parse.urlsplit(tmp).netloc for tmp in feeds]
	for feed in feeds:
		if not fnl.getNiceName(feed):
			netloc = urllib.parse.urlsplit(feed).netloc
			title = netloc
			if fetchTitle:
				title = get_page_title(wg, feed)
			print('Missing: "%s" %s: "%s",' % (netloc, " " * (50 - len(netloc)), title))

def exposed_delete_feed(feed_name, do_delete, search_str):
	'''
	Feed name is the readable name of the feed, from feedNameLut.py.
	do delete is a boolean that determines if the deletion is actually done, or the actions are
		just previewed. Unless do_delete.lower() == "true", no action will actually be
		taken.
	search_str is the string of items to search for. Searches are case sensitive, and the only
		component of the feed that are searched within is the title.
		search_str is split on the literal character "|", for requiring multiple substrings
		be in the searched title.

	Delete the rss entries for a feed, using a search key.

	'''

	sess = db.get_db_session()
	items = sess.query(db.FeedItems)               \
		.filter(db.FeedItems.srcname == feed_name) \
		.all()

	do_delete = "true" in do_delete.lower()

	searchitems = search_str.split("|")
	for item in items:
		itemall = " ".join([item.title] + item.tags)
		if all([searchstr in itemall for searchstr in searchitems]):
			print(itemall)
			if do_delete:
				print("Deleting item")
				sess.delete(item)

	sess.commit()


def exposed_nu_new():
	'''
	Parse outbound netlocs from NovelUpdates releases, extracting
	any sites that are not known in the feednamelut.
	'''

	import WebMirror.OutputFilters.util.feedNameLut as fnl
	sess = db.get_db_session()

	nu_items = sess.query(db.NuReleaseItem)             \
		.filter(db.NuReleaseItem.validated == True)     \
		.filter(db.NuReleaseItem.actual_target != None) \
		.all()

	netlocs = [urllib.parse.urlsplit(row.actual_target).netloc for row in nu_items]
	print("Nu outbound items: ", len(netlocs))
	netlocs = set(netlocs)

	missing = 0
	for netloc in netlocs:
		if not fnl.getNiceName(None, netloc):
			fnl.getNiceName(None, netloc, debug=True)
			print("Missing: ", netloc)
			missing += 1
	print("Nu outbound items: ", len(netlocs), "missing:", missing)


def exposed_fetch_other_feed_sources():
	'''
	Walk the listed pages for both AhoUpdates and NovelUpdates,
	retreiving a list of the translators from each.
	'''
	WebMirror.SiteSync.fetch.fetch_other_sites()


def exposed_fix_missing_history():
	'''
	Fix any items that don't have an entry in the history table.
	'''
	Misc.HistoryAggregator.Consolidate.fix_missing_history()

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
	Testing function for NewJobQueue components
	'''

	instance = WebMirror.NewJobQueue.JobAggregatorInternal(None, None)

	want = instance.outbound_job_wanted("www.novelupdates.com", "http://www.novelupdates.com/")
	print(want)
	want = instance.outbound_job_wanted("twitter.com", "https://twitter.com/Baka_Tsuki")
	print(want)
	want = instance.outbound_job_wanted("twitter.com", "https://twitter.com/Nano_Desu_Yo")
	print(want)


def exposed_drop_priorities():
	'''
	Reset the priority of every row in the table to the IDLE_PRIORITY level
	'''

	step  = 10000

	sess = db.get_db_session()
	print("Getting minimum row in need or update..")
	start = sess.execute("""SELECT min(id) FROM web_pages WHERE priority < 500000""")
	start = list(start)[0][0]
	print("Minimum row ID: ", start, "getting maximum row...")
	stop = sess.execute("""SELECT max(id) FROM web_pages WHERE priority < 500000""")
	stop = list(stop)[0][0]
	print("Maximum row ID: ", stop)

	if not start:
		print("No null rows to fix!")
		return

	print("Need to fix rows from %s to %s" % (start, stop))
	start = start - (start % step)

	changed = 0
	for idx in range(start, stop, step):
		try:
			# SQL String munging! I'm a bad person!
			# Only done because I can't easily find how to make sqlalchemy
			# bind parameters ignore the postgres specific cast
			# The id range forces the query planner to use a much smarter approach which is much more performant for small numbers of updates
			have = sess.execute("""update web_pages set priority = 500000 where priority < 500000 AND id > {} AND id <= {};""".format(idx, idx+step))
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


	sess.commit()
