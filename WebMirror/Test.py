

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
	ret = archiver.fetch(new)

	if debug:
		print(archiver)
		print(ret.keys())

		if "plainLinks" in ret and "rsrcLinks" in ret: # Looks like a HTML page. Print the relevant info
			print_html_response(archiver, new, ret)
		if "rss-content" in ret:
			print_rss_response(archiver, new, ret)


	# cmd = text("""
	# 		INSERT INTO
	# 			web_pages
	# 			(url, starturl, netloc, distance, is_text, priority, type, fetchtime)
	# 		VALUES
	# 			(:url, :starturl, :netloc, :distance, :is_text, :priority, :type, :fetchtime)
	# 		ON CONFLICT DO NOTHING
	# 		""")
	# print("doing")
	# ins = archiver.db.get_session().execute(cmd, params=new)
	# print("Done. Ret:")
	# print(ins)
	# print(archiver.resetDlstate())
	# print(archiver.getTask())
	# print(archiver.getTask())
	# print(archiver.getTask())
	# print(archiver.taskProcess())
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


def decode(*args):
	print("Args:", args)

	if len(args) == 1:
		op = args[0]
		if op == "rss":
			test_all_rss()
		else:
			print("ERROR: Unknown command!")

	if len(args) == 2:
		op  = args[0]
		tgt = args[1]

		if op == "fetch":
			print("Fetch command! Retreiving content from URL: '%s'" % tgt)
			test(tgt)
		else:
			print("ERROR: Unknown command!")


if __name__ == "__main__":
	import sys
	if len(sys.argv) < 2:

		print("you must pass a operation to execute!")
		sys.exit(1)

	decode(*sys.argv[1:])
	# test("http://www.royalroadl.com/fiction/1484")


