

if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()

import WebMirror.database as db
import datetime
from WebMirror.Engine import SiteArchiver
import urllib.parse
import urllib.error
import WebMirror.rules
import flags
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

def test(url, debug=True):

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
	ret = archiver.taskProcess(job_test=new)

	if debug:
		print(archiver)
		print(ret.keys())

		if "plainLinks" in ret and "rsrcLinks" in ret: # Looks like a HTML page. Print the relevant info
			print_html_response(archiver, new, ret)
		if "rss-content" in ret:
			print_rss_response(archiver, new, ret)


	pass

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




def decode(*args):
	print("Args:", args)

	if len(args) == 1:
		op = args[0]
		if op == "rss":
			test_all_rss()
		elif op == "db-fiddle":
			db_fiddle()
		elif op == "longest-rows":
			longest_rows()
		else:
			print("ERROR: Unknown command!")

	if len(args) == 2:
		op  = args[0]
		tgt = args[1]

		if op == "fetch":
			print("Fetch command! Retreiving content from URL: '%s'" % tgt)
			test(tgt)
		elif op == "fetch-silent":
			print("Fetch command! Retreiving content from URL: '%s'" % tgt)
			test(tgt, debug=False)

		else:
			print("ERROR: Unknown command!")


if __name__ == "__main__":
	import sys
	if len(sys.argv) < 2:

		print("you must pass a operation to execute!")
		print("Current actions:")
		print('	rss')
		print('	db-fiddle')
		print('	longest-rows')
		print('	fetch {url}')
		print('	fetch-silent {url}')
		sys.exit(1)

	decode(*sys.argv[1:])
	# test("http://www.royalroadl.com/fiction/1484")


