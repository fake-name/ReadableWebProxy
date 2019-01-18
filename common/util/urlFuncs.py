
import re
import urllib.parse
import re
import unshortenit

import requests.exceptions

import common.database as db

# All tags you need to look into to do link canonization
# source: http://stackoverflow.com/q/2725156/414272
# "These aren't necessarily simple URLs ..."
urlContainingTargets = [
	(False, 'a',          'href'),
	(False, 'applet',     'codebase'),
	(False, 'area',       'href'),
	(False, 'base',       'href'),
	(False, 'blockquote', 'cite'),
	(False, 'body',       'background'),
	(False, 'del',        'cite'),
	(False, 'form',       'action'),
	(False, 'frame',      'longdesc'),
	(False, 'frame',      'src'),
	(False, 'head',       'profile'),
	(False, 'iframe',     'longdesc'),
	(False, 'iframe',     'src'),
	(False, 'input',      'src'),
	(False, 'input',      'usemap'),
	(False, 'ins',        'cite'),
	(False, 'link',       'href'),
	(False, 'object',     'classid'),
	(False, 'object',     'codebase'),
	(False, 'object',     'data'),
	(False, 'object',     'usemap'),
	(False, 'q',          'cite'),
	(False, 'script',     'src'),
	(False, 'audio',      'src'),
	(False, 'button',     'formaction'),
	(False, 'command',    'icon'),
	(False, 'embed',      'src'),
	(False, 'html',       'manifest'),
	(False, 'input',      'formaction'),
	(False, 'source',     'src'),
	(False, 'video',      'poster'),
	(False, 'video',      'src'),
	(True,  'img',        'longdesc'),
	(True,  'img',        'src'),
	(True,  'img',        'usemap'),
]


gdocBaseReExt = re.compile(r'(https?://docs.google.com/document/d/[-_0-9a-zA-Z]+(?:/pub)?)(.*)$')

def trimGDocUrl(rawUrl):
	# if "docs.google.com" in rawUrl:
	# 	print("Trimming URL: ", rawUrl)

	url = rawUrl.split("#")[0]


	urlParam = urllib.parse.urlparse(url)

	# Short circuit so we don't munge non-google URLs
	if not 'google.com' in urlParam.netloc:
		return rawUrl

	qArr = urllib.parse.parse_qs(urlParam.query)
	if urlParam.query and 'google.com' in urlParam.netloc:
		qArr.pop('usp', None)
		qArr.pop('pli', None)
		qArr.pop('authuser', None)
		if qArr:
			queryStr = urllib.parse.urlencode(qArr, doseq=True)
		else:
			queryStr = ''
	else:
		# Unfortunately, parsing and re-encoding can reorder the parameters in the URL.
		# Since there is some idiot-checking to see if the url has changed if it /shouldn't/
		# and reodering would break that, we don't just use urlencode by default, unless it's
		# actually changed anything.
		queryStr = urlParam.query

	# This trims off any fragment, and re-adds the query-string(if present) with any google keys removed
	# print(urlParam, (queryStr, ''))
	params = urlParam[:4] + (queryStr, '')
	# print("Params", params)
	url = urllib.parse.urlunparse(params)

	# If the url has 'preview/' on the end, chop that off (but only for google content)
	if 'docs.google.com' in urlParam.netloc:
		strip = [
			"/preview/",
			"/preview",
			"/edit",
			"/view",
			"/mobilebasic",
			"/mobilebasic?viewopt=127",
			"?embedded=true",
			"?embedded=false",
			]

		simpleCheck = gdocBaseReExt.search(url)
		if simpleCheck:
			# print("SimpleCheck: ", simpleCheck, simpleCheck.groups())
			if any([item in simpleCheck.group(2) for item in strip]):
				url = simpleCheck.group(1)

		for ending in strip:
			if url.endswith(ending):
				url = url[:-len(ending)]

	# if "docs.google.com" in url:
	# 	print("Trimmed URL: ", url)

	# if url.endswith("/pub"):
	# 	url = url[:-3]


	return url

gdocBaseRe = re.compile(r'(https?://docs\.google\.com/document/d/[-_0-9a-zA-Z]+)')
driveToDocRe = re.compile(r'https?://drive\.google\.com/open\?id=([-_0-9a-zA-Z]+)')

def isGdocUrl(url):
	simpleCheck = gdocBaseRe.search(url)
	if simpleCheck and not url.endswith("/pub"):
		# return True, simpleCheck.group(1)
		return True, trimGDocUrl(url)

	simpleCheck = driveToDocRe.search(url)
	if simpleCheck and not url.endswith("/pub"):
		print("URL Group:", simpleCheck.group(1))
		# return True, simpleCheck.group(1)
		return True, "https://docs.google.com/document/d/{}".format(simpleCheck.group(1))



	return False, url

gFileBaseRe = re.compile(r'(https?://docs.google.com/file/d/[-_0-9a-zA-Z]+)')

def isGFileUrl(url):

	simpleCheck = gFileBaseRe.search(url)
	if simpleCheck and not url.endswith("/pub"):
		return True, trimGDocUrl(url)

	scheme, netloc, path, params, query, fragment = urllib.parse.urlparse(url)

	if netloc == 'drive.google.com' and path == '/folderview':
		query = urllib.parse.parse_qsl(query)
		query = [item for item in query if item[0] != "usp"]
		query.sort()
		query = urllib.parse.urlencode(query)

		url = urllib.parse.urlunparse((scheme, netloc, path, params, query, fragment))
		return True, url

	return False, url


##############################################################################################################
##############################################################################################################
##############################################################################################################
##############################################################################################################

class CacheObject():
	def __setitem__(self, key, item):
		db.set_in_db_key_value_store(key, item)

	def __getitem__(self, key):
		return db.get_from_db_key_value_store(key)

	def __delitem__(self, key):
		db.set_in_db_key_value_store(key, {})

	def get(self, key, default="super_sekrit_not_specified_value"):
		ret = db.get_from_db_key_value_store(key)
		if ret:
			return ret
		if default != "super_sekrit_not_specified_value":
			return default
		raise KeyError("Key %s not found in CacheObject backing store!" % (key, ))

	def clear(self):
		raise ValueError("Cannot clear a CacheObject")

	def copy(self):
		raise ValueError("Cannot copy a CacheObject")

	def has_key(self, k):
		return db.get_from_db_key_value_store(k) != {}

SQUATTER_NETLOC_RE = re.compile(r"^www?\d+\.")

def cleanUrl(urlin):
	# Fucking tumblr redirects.
	if urlin.startswith("https://www.tumblr.com/login"):
		return None

	resolve_redirects = False

	parsed = urllib.parse.urlparse(urlin)
	if SQUATTER_NETLOC_RE.match(parsed.netloc):
		print("Regex rejecting url: ", urlin)
		return None

	if 'wp.me' in parsed.netloc:
		resolve_redirects = True

	try:

		url = unshortenit.UnshortenIt(urlcache=CacheObject()).unshorten(urlin, resolve_30x=resolve_redirects)
		return url
	except (unshortenit.NotFound, unshortenit.UnshortenFailed, requests.exceptions.ConnectionError):
		return None

	return urlin


##############################################################################################################
##############################################################################################################
##############################################################################################################
##############################################################################################################

def rebaseUrl(url, base):
	"""Rebase one url according to base"""

	parsed = urllib.parse.urlparse(url)
	if parsed.scheme == '' or parsed.netloc == '':
		return urllib.parse.urljoin(base, url)
	else:
		return url

def canonizeUrls(soup, pageUrl):
	# print("Canonizing for page: ", pageUrl)
	for (dummy_isimg, tag, attr) in urlContainingTargets:
		for link in soup.findAll(tag):
			try:
				url = link[attr]
			except KeyError:
				pass
			else:
				link[attr] = rebaseUrl(url, pageUrl)

	return soup

def extractUrls(soup, pageUrl, truncate_fragment=False):
	# print("Canonizing for page: ", pageUrl)
	urls = set()
	for (dummy_isimg, tag, attr) in urlContainingTargets:
		for link in soup.findAll(tag):
			try:
				url = link[attr]
			except KeyError:
				pass
			else:

				if url.startswith("javascript"):
					continue
				if url.startswith("data:"):
					continue
				if url.startswith("ios-app:"):
					continue
				if url.startswith("clsid:"):
					continue
				if url.startswith("mailto:"):
					continue
				fixed = rebaseUrl(url, pageUrl)
				assert fixed.startswith("http"), "Wat?: '%s', '%s', '%s'" % (url, pageUrl, fixed)
				urls.add(fixed)
	if truncate_fragment:
		ret = set()
		for url in urls:
			split = urllib.parse.urlsplit(url)
			if split.fragment:
				fixed = urllib.parse.urlunsplit(split[:4] + ("", ) + split[5:])
				# print("Fixed: ", fixed)
				ret.add(fixed)
			else:
				ret.add(url)
		return ret
	return urls


def hasDuplicateSegments(url):

		parsed = urllib.parse.urlsplit(url)
		netloc = parsed.netloc
		if not netloc:
			print("Wat? No netloc for URL: %s" % url)
			return True

		pathchunks = parsed.path.split("/")
		pathchunks = [chunk for chunk in pathchunks if chunk]

		# http://www.spcnet.tv/forums/showthread.php/21185-mobile-suit-gundam-the-second-century-(part-2-the-second-century)/images/icons/images/misc/showthread.php/21185-Mobile-Suit-Gundam-The-Second-Century-(Part-2-The-Second-Century)/page10
		if netloc == 'www.spcnet.tv' or netloc == 'www.eugenewoodbury.com':
			# Yeah, special case stuff because spcnet is garbage.

			# Block instances where there are multiple known-bad segments.
			disallow_multiple = [
				'images',
				'avatars',
				'smilies',
				]
			if any([pathchunks.count(i) > 1 for i in disallow_multiple]):
				return True

			# Block a url where multiple instances of the php page is present.
			disalow_several = [
				'cron.php',
				'external.php',
				'forumdisplay.php',
				'member.php',
				'register.php',
				'showthread.php',
			]

			if sum([pathchunks.count(i) for i in disalow_several]) > 1:
				return True

			# ON SPCnet, the value in the path after the .php file is the target
			# page ID. Any path after the page id is basically ignored.
			# As such, it'll basically wind up being a duplicate, since they
			# all redirect to the same place.
			# Therefore, we handle (and ignore) pages with lots of duplicates.
			for bad_chunk in disalow_several:
				try:
					idx = pathchunks.index(bad_chunk)
					if len(pathchunks) - idx > 2:
						print("Bad:", pathchunks, idx)
						return True
				except ValueError:
					pass


		# http://www.spcnet.tv/forums/showthread.php/21185-mobile-suit-gundam-the-second-century-(part-2-the-second-century)/images/icons/images/misc/showthread.php/21185-Mobile-Suit-Gundam-The-Second-Century-(Part-2-The-Second-Century)/page10
		if netloc == 'www.eugenewoodbury.com':

			# Block a url where multiple instances of the php page is present.
			disalow_several = [

				'angel',
				'biblio',
				'essays',
				'foxwolf',
				'image',
				'kasho',
				'paradise',
				'path',
				'serpent',
				'wind',
			]

			if sum([pathchunks.count(i) for i in disalow_several]) > 1:
				return True

		if 'www.wastedtalent.ca' in url:
			bulkchunks = url.split("/")
			bulkchunks = [chunk for chunk in bulkchunks if chunk]
			bduplicates = list(set([(i, bulkchunks.count(i)) for i in bulkchunks if bulkchunks.count(i) > 1]))

			if any([cnt > 3 for (item, cnt) in bduplicates]):
				print("Bulk duplicates issue: %s - %s" % (url, (pathchunks, set(pathchunks))))
				return True


		if netloc == 'archiveofourown.org' or netloc == 'www.archiveofourown.org':
			if "feed.atom" in url:
				return True

		if netloc == 'creativenovels.com' and url.count("/") >= 5 and url.endswith("/feed/"):
			# Goddammit wordpress
			return False

		if len(set(pathchunks)) != len(pathchunks):

			duplicates = list(set([(i, pathchunks.count(i)) for i in pathchunks if pathchunks.count(i) > 1]))

			if any([cnt > 3 for (item, cnt) in duplicates]):
				# print("Pathchunks issue: %s - %s" % (url, (pathchunks, set(pathchunks))))
				return True
			if len(duplicates) > 3:
				# print("Pathchunks issue: %s - %s" % (url, (pathchunks, set(pathchunks))))
				return True


		querydict = urllib.parse.parse_qs(parsed.query)

		querychunks = []
		for key in querydict.keys():
			for value in querydict[key]:
				querychunks.append((key, value))

		qduplicates = list(set([(i, querychunks.count(i)) for i in querychunks if querychunks.count(i) > 1]))
		if any([cnt > 3 for (item, cnt) in qduplicates]):
			# print("Query chunks issue: %s - %s" % (url, (querychunks, set(querychunks))))
			# print("Thing: ", [cnt > 3 for (item, cnt) in qduplicates], qduplicates)
			return True

		return False



def urlClean(url):
	assert url != None
	# Google docs can be accessed with or without the '/preview' postfix
	# We want to remove this if it's present, so we don't duplicate content.
	url = trimGDocUrl(url)
	url = cleanUrl(url)

	if url is None:
		return None

	while True:
		url2 = urllib.parse.unquote(url)
		url2 = url2.split("#")[0]
		if url2 == url:
			break
		url = url2

	# Clean off whitespace.
	url = url.strip()

	return url

def getNetLoc(url):
	parsed = urllib.parse.urlparse(url)
	if not parsed.netloc:
		raise ValueError("No netloc in url: '{}'".format(url))
	return parsed.netloc

if __name__ == "__main__":

	# print(isGFileUrl('https://drive.google.com/folderview?id=0B_mXfd95yvDfQWQ1ajNWZTJFRkk&usp=drive_web'))
	# print(urlClean('http://inmydaydreams.com/?p=6128&share=tumblr'))
	# print(urlClean('http://inmydaydreams.com/?p=6091&share=tumblr'))

	print(hasDuplicateSegments('http://www.spcnet.tv/forums/showthread.php/23450-i-ve-decided-to-learn-chinese/index/images/misc/image.php?s=1129386e978631b0771a226dba5a82e5&u=65&dateline=1358455669'))
	# print(hasDuplicateSegments('http://inmydaydreams.com/?p=6091&share=tumblr'))

	# print(hasDuplicateSegments(
	# 	"http://deadlynovels.com/community/recent/?view=unread?type=rss2&forum=g&topic=g?type=rss2&forum=g&"
	# 	"topic=g?type=rss2&forum=g?type=rss2&forum=g&topic=g?type=rss2&forum=g&topic=g?type=rss2&forum=g?"
	# 	"type=rss2&forum=g&topic=g?type=rss2&forum=g?type=rss2&forum=g?type=rss2&forum=g&topic=g?type=rss2"
	# 	"&forum=g?type=rss2&forum=g&topic=g?type=rss2&forum=g?type=rss2&forum=g&topic=g?type=rss2&forum=g"
	# 	"?type=rss2&forum=g?type=rss2&forum=g?type=rss2&forum=g&topic=g?type=rss2&forum=g?type=rss2&forum=g"
	# 	"&topic=g?type=rss2&forum=g?type=rss2&forum=g?type=rss2&forum=g?type=rss2&forum=g&topic=g?type=rss2"
	# 	"&forum=g&topic=g?type=rss2&forum=g&topic=g?type=rss2&forum=g&topic=g?type=rss2&forum=g&topic=g?type=rss2"
	# 	"&forum=g&topic=g?type=rss2&forum=g&topic=g?type=rss2&forum=g&topic=g?type=rss2&forum=g?type=rss2&forum=g"
	# 	"?type=rss2&forum=g&topic=g?type=rss2&forum=g?type=rss2&forum=g&topic=g?type=rss2&forum=g?type=rss2"
	# 	"&forum=g?type=rss2&forum=g&topic=g?type=rss2&forum=g&topic=g?type=rss2&forum=g&topic=g?type=rss2"
	# 	"&forum=g&topic=g?type=rss2&forum=g&topic=g?type=rss2&forum=g"))

