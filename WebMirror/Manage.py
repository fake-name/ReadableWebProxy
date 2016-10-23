

if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()

import common.database as db
import datetime
from WebMirror.Engine import SiteArchiver
from concurrent.futures import ThreadPoolExecutor
import sqlalchemy.exc
import traceback
import os
import os.path
import config
import calendar
import json
import WebMirror.OutputFilters.util.feedNameLut as feedNameLut
import urllib.parse
import urllib.error
import WebMirror.rules
import flags
import WebMirror.SiteSync.fetch
from sqlalchemy import or_
from sqlalchemy import and_
import common.Exceptions
import WebMirror.SpecialCase
import RawArchiver.RawActiveModules

from sqlalchemy_continuum.utils import version_table

import Misc.HistoryAggregator.Flatten



def exposed_test_retrieve(url, debug=True, rss_debug=False):
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
	exposed_test_retrieve(tgt, debug=False)

def exposed_fetch_rss(tgt):
	'''
	Identical to `test_retrieve`, except debug printing is supressed and RSS debugging is enabled.
	'''
	exposed_test_retrieve(tgt, debug=False, rss_debug=True)


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
	print("fetching and debugging RSS feeds")
	rules = WebMirror.rules.load_rules()
	feeds = [item['feedurls'] for item in rules]
	feeds = [item for sublist in feeds for item in sublist]

	flags.RSS_DEBUG = True
	with ThreadPoolExecutor(max_workers=8) as executor:
		for url in feeds:
			try:
				executor.submit(exposed_test_retrieve, url, debug=False)
			except common.Exceptions.DownloadException:
				print("failure downloading page!")
			except urllib.error.URLError:
				print("failure downloading page!")

def exposed_db_fiddle():
	print("Fixing DB things.")
	print("Getting IDs")
	have = db.get_db_session().execute("""
		SELECT id FROM web_pages WHERE url LIKE 'https://www.wattpad.com/story%' AND state != 'new';
		""")
	print("Query executed. Fetching results")
	have = list(have)
	print(len(have))
	count = 0

	chunk = []
	for item, in have:
		chunk.append(item)

		count += 1
		if count % 1000 == 0:
			statement = db.get_db_session().query(db.WebPages) \
				.filter(db.WebPages.state != 'new')        \
				.filter(db.WebPages.id.in_(chunk))

			# statement = db.get_db_session().update(db.WebPages)
			statement.update({db.WebPages.state : 'new'}, synchronize_session=False)
			chunk = []
			print(count, item)
			db.get_db_session().commit()

def exposed_longest_rows():
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

def exposed_fix_tsv():
	step = 1000


	print("Determining extents that need to be changed.")
	start = db.get_db_session().execute("""SELECT MIN(id) FROM web_pages WHERE tsv_content IS NULL AND content IS NOT NULL AND id != 60903982;""")
	start = list(start)[0][0]

	end = db.get_db_session().execute("""SELECT MAX(id) FROM web_pages WHERE tsv_content IS NULL AND content IS NOT NULL;""")
	end = list(end)[0][0]

	changed = 0
	print("Start: ", start)
	print("End: ", end)


	if not start:
		print("No null rows to fix!")
		return

	start = start - (start % step)

	for x in range(start, end, step):
		try:
			# SQL String munging! I'm a bad person!
			# Only done because I can't easily find how to make sqlalchemy
			# bind parameters ignore the postgres specific cast
			# The id range forces the query planner to use a much smarter approach which is much more performant for small numbers of updates
			have = db.get_db_session().execute("""UPDATE web_pages SET tsv_content = to_tsvector(coalesce(content)) WHERE tsv_content IS NULL AND content IS NOT NULL AND id < %s AND id >= %s;""" % (x, x-step))
			# print()
			print('%10i, %10i, %7.4f, %6i' % (x, end, (x-start)/(end-start) * 100, have.rowcount))
			changed += have.rowcount
			if changed > step:
				print("Committing (%s changed rows)...." % changed, end=' ')
				db.get_db_session().commit()
				print("done")
				changed = 0
		except sqlalchemy.exc.OperationalError:
			db.get_db_session().rollback()
			print("Error!")
			traceback.print_exc()

	db.get_db_session().commit()

def exposed_disable_wattpad():
	step = 50000


	print("Determining extents that need to be changed.")
	start = db.get_db_session().execute("""
		SELECT
			MIN(id)
		FROM
			web_pages
		WHERE
			(netloc = 'www.wattpad.com' OR netloc = 'a.wattpad.com')
		;""")

	start = list(start)[0][0]
	print("Start: ", start)

	end = db.get_db_session().execute("""
		SELECT
			MAX(id)
		FROM
			web_pages
		WHERE
			(netloc = 'www.wattpad.com' OR netloc = 'a.wattpad.com')
		;""")
	end = list(end)[0][0]

	changed = 0
	print("End: ", end)


	if not start:
		print("No null rows to fix!")
		return

	start = start - (start % step)

	for x in range(start, end, step):
		try:
			# SQL String munging! I'm a bad person!
			# Only done because I can't easily find how to make sqlalchemy
			# bind parameters ignore the postgres specific cast
			# The id range forces the query planner to use a much smarter approach which is much more performant for small numbers of updates
			have = db.get_db_session().execute("""
				UPDATE
					web_pages
				SET
					state = 'disabled'
				WHERE
						(netloc = 'www.wattpad.com' OR netloc = 'a.wattpad.com')
					AND
						(state = 'new' OR state = 'fetching' OR state = 'processing')
					AND
						id < %s
					AND
						id >= %s;""" % (x, x-step))
			# print()
			print('%10i, %10i, %10i, %7.4f, %6i' % (start, x, end, (x-start)/(end-start) * 100, have.rowcount))
			changed += have.rowcount
			if changed > step / 2:
				print("Committing (%s changed rows)...." % changed, end=' ')
				db.get_db_session().commit()
				print("done")
				changed = 0
		except sqlalchemy.exc.OperationalError:
			db.get_db_session().rollback()
			print("Error!")
			traceback.print_exc()

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

def exposed_delete_comment_feed_items():

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

def exposed_purge_invalid_urls(selected_netloc=None):


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

# Re-order the missed file list by order of misses.
def exposed_sort_json(json_name):
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
			for value in item[2]:
				for key in key_order:
					fp.write("%s, " % ((key, value[key]), ))
				fp.write("\n")

# Re-order the missed file list by order of misses.
def exposed_sort_thing(json_name):
	with open(json_name) as fp:
		cont = fp.readlines()
	print("Json file has %s lines." % len(cont))

	data = {}
	for line in cont:
		val = json.loads(line.replace("'", '"'))
		name = val['nu_release']['groupinfo']
		if not name in data:
			data[name] = []

		data[name].append(val)
	out = []
	for key in data:
		out.append((len(data[key]), data[key]))

	out.sort(key=lambda x: (x[0], x[1]*-1))
	out.sort(key=lambda x: (x[1]*-1))

	key_order = [
		'groupinfo',
		'seriesname',
		'releaseinfo',
		'actual_target',
		'addtime',
		'outbound_wrapper',
		'referrer',
	]

	outf = json_name+".pyout"
	try:
		os.unlink(outf)
	except FileNotFoundError:
		pass

	with open(outf, "w") as fp:
		for item in out:
			# print(item[1])
			for value in item[1]:
				for key in key_order:
					fp.write("%s, " % ((key, value['nu_release'][key]), ))
				fp.write("\n")

def exposed_rss_db_sync(target = None, days=False, silent=False):

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
	exposed_rss_db_sync(silent=True)

def exposed_rss_day():
	exposed_rss_db_sync(days=1)

def exposed_rss_week():
	exposed_rss_db_sync(days=7)

def exposed_rss_month():
	exposed_rss_db_sync(days=45)


def exposed_clear_blocked():
	for ruleset in WebMirror.rules.load_rules():
		if ruleset['netlocs'] and ruleset['badwords']:
			# mask = [db.WebPages.url.like("%{}%".format(tmp)) for tmp in ruleset['badwords'] if not "%" in tmp]

			for badword in ruleset['badwords']:
				feed_items = db.get_db_session().query(db.WebPages)          \
					.filter(db.WebPages.netloc.in_(ruleset['netlocs']))   \
					.filter(db.WebPages.url.like("%{}%".format(badword))) \
					.count()

				if feed_items:
					print("Have:  ", feed_items, badword)
					feed_items = db.get_db_session().query(db.WebPages)          \
						.filter(db.WebPages.netloc.in_(ruleset['netlocs']))   \
						.filter(db.WebPages.url.like("%{}%".format(badword))) \
						.delete(synchronize_session=False)
					db.get_db_session().expire_all()

				else:
					print("Empty: ", feed_items, badword)
			# print(mask)
			# print(ruleset['netlocs'])
			# print(ruleset['badwords'])

def exposed_filter_links(path):
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

def exposed_missing_lut():
	import WebMirror.OutputFilters.util.feedNameLut as fnl
	rules = WebMirror.rules.load_rules()
	feeds = [item['feedurls'] for item in rules]
	feeds = [item for sublist in feeds for item in sublist]
	# feeds = [urllib.parse.urlsplit(tmp).netloc for tmp in feeds]
	for feed in feeds:
		if not fnl.getNiceName(feed):
			print("Missing: ", urllib.parse.urlsplit(feed).netloc)

def exposed_delete_feed(feed_name, do_delete, search_str):

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

def exposed_consolidate_history():
	Misc.HistoryAggregator.Flatten.consolidate_history()
