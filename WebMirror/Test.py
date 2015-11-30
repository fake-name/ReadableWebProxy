

if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()

# This HAS to be included before the app, to prevent circular dependencies.
import WebMirror.runtime_engines

import WebMirror.database as db
import datetime
from WebMirror.Engine import SiteArchiver

import sqlalchemy.exc
import traceback
import settings
import config
import calendar
from sqlalchemy import and_
from sqlalchemy.sql import text
import WebMirror.OutputFilters.util.feedNameLut as feedNameLut
import urllib.parse
import urllib.error
import WebMirror.rules
import flags
from sqlalchemy import or_
import WebMirror.Exceptions

def print_html_response(archiver, new, ret):
	print("Plain links:")
	for link in ret['plainLinks']:
		print("	'%s'" % link.replace("\n", ""))
	print("Resource links:")
	for link in ret['rsrcLinks']:
		print("	'%s'" % link.replace("\n", ""))

	print()
	print("Filtering")
	badwords = archiver.getBadWords(new)
	filtered = archiver.filterContentLinks(new, ret['plainLinks'], badwords)
	filteredr = archiver.filterContentLinks(new, ret['rsrcLinks'], badwords)

	print("Filtered plain links:")
	for link in filtered:
		print("	'%s'" % link.replace("\n", ""))
	print("Filtered resource links:")
	for link in filteredr:
		print("	'%s'" % link.replace("\n", ""))

def print_rss_response(archiver, new, ret):
	pass

def test(url, debug=True, rss_debug=False):
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
	archiver = SiteArchiver(None)
	archiver.taskProcess(job_test=new)

	# if debug:
	# 	print(archiver)
	# 	print(ret.keys())

	# 	if "plainLinks" in ret and "rsrcLinks" in ret: # Looks like a HTML page. Print the relevant info
	# 		print_html_response(archiver, new, ret)
	# 	if "rss-content" in ret:
	# 		print_rss_response(archiver, new, ret)



def test_all_rss():
	print("fetching and debugging RSS feeds")
	rules = WebMirror.rules.load_rules()
	feeds = [item['feedurls'] for item in rules]
	feeds = [item for sublist in feeds for item in sublist]

	flags.RSS_DEBUG = True
	for url in feeds:
		try:
			test(url, debug=False)
		except WebMirror.Exceptions.DownloadException:
			print("failure downloading page!")
		except urllib.error.URLError:
			print("failure downloading page!")

def db_fiddle():
	print("Fixing DB things.")
	print("Getting IDs")
	have = db.get_session().execute("""
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


			statement = db.get_session().query(db.WebPages) \
				.filter(db.WebPages.state != 'new')        \
				.filter(db.WebPages.id.in_(chunk))

			# statement = db.get_session().update(db.WebPages)
			statement.update({db.WebPages.state : 'new'}, synchronize_session=False)
			chunk = []
			print(count, item)
			db.get_session().commit()

def longest_rows():
	print("Getting longest rows from database")
	have = db.get_session().execute("""
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


def fix_null():
	step = 50000


	end = db.get_session().execute("""SELECT MAX(id) FROM web_pages WHERE  ignoreuntiltime IS NULL;""")
	end = list(end)[0][0]

	start = db.get_session().execute("""SELECT MIN(id) FROM web_pages WHERE ignoreuntiltime IS NULL;""")
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
		have = db.get_session().execute("""UPDATE web_pages SET ignoreuntiltime = 'epoch'::timestamp WHERE ignoreuntiltime IS NULL AND id < %s AND id >= %s;""" % (x, x-step))
		# print()
		print('%10i, %7.4f, %6i' % (x, x/end * 100, have.rowcount))
		changed += have.rowcount
		if changed > 10000:
			print("Committing (%s changed rows)...." % changed, end=' ')
			db.get_session().commit()
			print("done")
			changed = 0
	db.get_session().commit()


def fix_tsv():
	step = 1000


	print("Determining extents that need to be changed.")
	start = db.get_session().execute("""SELECT MIN(id) FROM web_pages WHERE tsv_content IS NULL AND content IS NOT NULL AND id != 60903982;""")
	start = list(start)[0][0]

	end = db.get_session().execute("""SELECT MAX(id) FROM web_pages WHERE tsv_content IS NULL AND content IS NOT NULL;""")
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
			have = db.get_session().execute("""UPDATE web_pages SET tsv_content = to_tsvector(coalesce(content)) WHERE tsv_content IS NULL AND content IS NOT NULL AND id < %s AND id >= %s;""" % (x, x-step))
			# print()
			print('%10i, %10i, %7.4f, %6i' % (x, end, (x-start)/(end-start) * 100, have.rowcount))
			changed += have.rowcount
			if changed > step:
				print("Committing (%s changed rows)...." % changed, end=' ')
				db.get_session().commit()
				print("done")
				changed = 0
		except sqlalchemy.exc.OperationalError:
			db.get_session().rollback()
			print("Error!")
			traceback.print_exc()

	db.get_session().commit()


def clear_bad():
	from sqlalchemy.dialects import postgresql

	rules = WebMirror.rules.load_rules()

	for ruleset in rules:

		# print(ruleset['netlocs'])
		# print(ruleset.keys())
		for badword in ruleset['badwords']:
			if not ruleset['netlocs']:
				continue
			if "%" in badword:
				print(badword)
			else:

				q = db.get_session().query(db.WebPages)                   \
					.filter(db.WebPages.netloc.in_(ruleset['netlocs']))   \
					.filter(db.WebPages.url.like("%{}%".format(badword)))
				items = q.count()
				if items:
					print("%s results for : '%s'" % (items, badword))

					q = db.get_session().query(db.WebPages)                   \
						.filter(db.WebPages.netloc.in_(ruleset['netlocs']))   \
						.filter(db.WebPages.url.like("%{}%".format(badword))) \
						.delete(synchronize_session=False)
					db.get_session().commit()



def delete_comment_feed_items():

	sess = db.get_session()
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



def update_feed_names():
	for key, value in feedNameLut.mapper.items():
		feed_items = db.get_session().query(db.FeedItems) \
				.filter(db.FeedItems.srcname == key)    \
				.all()
		if feed_items:
			for item in feed_items:
				item.srcname = value
			print(len(feed_items))
			print(key, value)
			db.get_session().commit()




def rss_db_sync(target = None):
	write_debug = True
	if target:
		config.C_DO_RABBIT = False
		flags.RSS_DEBUG    = True
		write_debug = False

	import WebMirror.processor.RssProcessor
	parser = WebMirror.processor.RssProcessor.RssProcessor(loggerPath   = "Main.RssDb",
															pageUrl     = 'http://www.example.org',
															pgContent   = '',
															type        = 'application/atom+xml',
															transfer    = False,
															debug_print = True,
															write_debug = write_debug)


	print("Getting feed items....")

	if target:
		print("Limiting to '%s' source." % target)
		feed_items = db.get_session().query(db.FeedItems) \
				.filter(db.FeedItems.srcname == target)    \
				.order_by(db.FeedItems.srcname)           \
				.order_by(db.FeedItems.title)           \
				.all()
	else:
		feed_items = db.get_session().query(db.FeedItems) \
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
			parser.processFeedData(ctnt, tx_raw=False)
		except ValueError:
			pass
		# print(ctnt)

def clear_blocked():
	for ruleset in WebMirror.rules.load_rules():
		if ruleset['netlocs'] and ruleset['badwords']:
			# mask = [db.WebPages.url.like("%{}%".format(tmp)) for tmp in ruleset['badwords'] if not "%" in tmp]

			for badword in ruleset['badwords']:
				feed_items = db.get_session().query(db.WebPages)          \
					.filter(db.WebPages.netloc.in_(ruleset['netlocs']))   \
					.filter(db.WebPages.url.like("%{}%".format(badword))) \
					.count()

				if feed_items:
					print("Have:  ", feed_items, badword)
					feed_items = db.get_session().query(db.WebPages)          \
						.filter(db.WebPages.netloc.in_(ruleset['netlocs']))   \
						.filter(db.WebPages.url.like("%{}%".format(badword))) \
						.delete(synchronize_session=False)
					db.get_session().expire_all()

				else:
					print("Empty: ", feed_items, badword)
			# print(mask)
			# print(ruleset['netlocs'])
			# print(ruleset['badwords'])
	pass


def decode(*args):
	print("Args:", args)

	if len(args) == 1:
		op = args[0]
		if op == "rss":
			test_all_rss()
		elif op == "rss-del-comments":
			delete_comment_feed_items()
		elif op == "db-fiddle":
			db_fiddle()
		elif op == "rss-name":
			update_feed_names()
		elif op == "longest-rows":
			longest_rows()
		elif op == "fix-null":
			fix_null()
		elif op == "fix-tsv":
			fix_tsv()
		elif op == "clear-bad":
			clear_bad()
		elif op == "rss-db":
			rss_db_sync()
		elif op == "clear-blocked":
			clear_blocked()
		else:
			print("ERROR: Unknown command!")

	if len(args) == 2:
		op  = args[0]
		tgt = args[1]

		if op == "fetch":
			print("Fetch command! Retreiving content from URL: '%s'" % tgt)
			test(tgt)
		elif op == "rss-db":
			rss_db_sync(tgt)
		elif op == "fetch-silent":
			print("Fetch command! Retreiving content from URL: '%s'" % tgt)
			test(tgt, debug=False)
		elif op == "fetch-rss":
			print("Fetch command! Retreiving content from URL: '%s'" % tgt)
			test(tgt, debug=False, rss_debug=True)

		else:
			print("ERROR: Unknown command!")


if __name__ == "__main__":
	import sys
	if len(sys.argv) < 2:

		print("you must pass a operation to execute!")
		print("Current actions:")
		print('	rss')
		print('	rss-del-comments')
		print('	rss-name')
		print('	db-fiddle')
		print('	longest-rows')
		print('	fix-null')
		print('	fix-tsv')
		print('	clear-bad')
		print('	clear-blocked')
		print('	rss-db')
		print('	rss-db {feedname}')
		print('	fetch {url}')
		print('	fetch-silent {url}')
		print('	fetch-rss {url}')
		sys.exit(1)

	decode(*sys.argv[1:])
	# test("http://www.royalroadl.com/fiction/1484")


