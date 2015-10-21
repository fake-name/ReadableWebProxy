
import re
import urllib.parse
import WebMirror.util.webFunctions

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

from WebMirror.Exceptions import CannotAccessGDocException



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

		gdocBaseRe = re.compile(r'(https?://docs.google.com/document/d/[-_0-9a-zA-Z]+(?:/pub)?)(.*)$')
		simpleCheck = gdocBaseRe.search(url)
		if simpleCheck:
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

def isGdocUrl(url):
	gdocBaseRe = re.compile(r'(https?://docs.google.com/document/d/[-_0-9a-zA-Z]+)')
	simpleCheck = gdocBaseRe.search(url)
	if simpleCheck and not url.endswith("/pub"):
		# return True, simpleCheck.group(1)
		return True, trimGDocUrl(url)

	return False, url


def isGFileUrl(url):

	gFileBaseRe = re.compile(r'(https?://docs.google.com/file/d/[-_0-9a-zA-Z]+)')
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






def clearOutboundProxy(url):
	'''
	So google proxies all their outbound links through a redirect so they can detect outbound links.
	This call strips them out if they are present.

	'''
	# 'https://www.google.com/url?sntz=1&q=https://bluesilvertranslations.wordpress.com/&usg=AFQjCNFzgp4e2VefkBwffciUm_xsCC4_zg&sa=D'?
	if url.startswith("http://www.google.com/url?"):
		qs = urllib.parse.urlparse(url).query
		query = urllib.parse.parse_qs(qs)
		if not "q" in query:
			raise ValueError("No target?")

		return query["q"].pop()

	return url



def clearBitLy(url):

	# Fucking tumblr redirects.
	if url.startswith("https://www.tumblr.com/login"):
		return None


	if "bit.ly" in url:
		wg = WebMirror.util.webFunctions.WebGetRobust(logPath="Main.BitLy.Web")
		try:

			dummy_ctnt, handle = wg.getpage(url, returnMultiple=True)
			# Recurse into redirects
			return clearBitLy(handle.geturl())

		except urllib.error.URLError:
			print("Error resolving redirect!")
			return None

	return url


def rebaseUrl(url, base):
	"""Rebase one url according to base"""

	parsed = urllib.parse.urlparse(url)

	if parsed.scheme == parsed.netloc == '':
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


def urlClean(url):
	# Google docs can be accessed with or without the '/preview' postfix
	# We want to remove this if it's present, so we don't duplicate content.
	url = trimGDocUrl(url)

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
	print('wat')

	print(isGFileUrl('https://drive.google.com/folderview?id=0B_mXfd95yvDfQWQ1ajNWZTJFRkk&usp=drive_web'))
