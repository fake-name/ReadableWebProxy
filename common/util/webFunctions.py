#!/usr/bin/python3
import sys
import codecs

try:
	import cchardet as chardet
except ImportError:
	import chardet as chardet

import http.client
import email.parser

import http.client
import email.parser

cchardet = False

try:
	import cchardet
except ImportError:
	pass

def isUTF8Strict(data):
	'''
	Check if all characters in a bytearray are decodable
	using UTF-8.
	'''
	try:
		decoded = data.decode('UTF-8')
	except UnicodeDecodeError:
		return False
	else:
		for ch in decoded:
			if 0xD800 <= ord(ch) <= 0xDFFF:
				return False
		return True

def decode_headers(header_list):
	'''
	Decode a list of headers.

	Takes a list of bytestrings, returns a list of unicode strings.
	The character set for each bytestring is individually decoded.
	'''

	decoded_headers = []
	for header in header_list:
		if cchardet:
			inferred = cchardet.detect(header)
			if inferred and inferred['confidence'] > 0.8:
				# print("Parsing headers!", header)
				decoded_headers.append(header.decode(inferred['encoding']))
			else:
				decoded_headers.append(header.decode('iso-8859-1'))
		else:
			# All bytes are < 127 (e.g. ASCII)
			if all([char & 0x80 == 0 for char in header]):
				decoded_headers.append(header.decode("us-ascii"))
			elif isUTF8Strict(header):
				decoded_headers.append(header.decode("utf-8"))
			else:
				decoded_headers.append(header.decode('iso-8859-1'))

	return decoded_headers


def parse_headers(fp, _class=http.client.HTTPMessage):
	"""Parses only RFC2822 headers from a file pointer.

	email Parser wants to see strings rather than bytes.
	But a TextIOWrapper around self.rfile would buffer too many bytes
	from the stream, bytes which we later need to read as bytes.
	So we read the correct bytes here, as bytes, for email Parser
	to parse.

	Note: Monkey-patched version to try to more intelligently determine
	header encoding

	"""
	headers = []
	while True:
		line = fp.readline(http.client._MAXLINE + 1)
		if len(line) > http.client._MAXLINE:
			raise http.client.LineTooLong("header line")
		headers.append(line)
		if len(headers) > http.client._MAXHEADERS:
			raise HTTPException("got more than %d headers" % http.client._MAXHEADERS)
		if line in (b'\r\n', b'\n', b''):
			break

	decoded_headers = decode_headers(headers)

	hstring = ''.join(decoded_headers)

	return email.parser.Parser(_class=_class).parsestr(hstring)

http.client.parse_headers = parse_headers


import urllib.request
import urllib.parse
import urllib.error
import socks
from sockshandler import SocksiPyHandler


import os.path

import time
import http.cookiejar

import traceback
import multiprocessing

import logging
import zlib
import bs4
import re
import string
import gzip
import string
import io
import socket
import json
import base64

import random
random.seed()


import selenium.webdriver.chrome.service
import selenium.webdriver.chrome.options
import selenium.webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities




def as_soup(str):
	return bs4.BeautifulSoup(str, "lxml")


def determine_json_encoding(json_bytes):
	'''
	Given the fact that the first 2 characters in json are guaranteed to be ASCII, we can use
	these to determine the encoding.
	See: http://tools.ietf.org/html/rfc4627#section-3

	Copied here:
	   Since the first two characters of a JSON text will always be ASCII
	   characters [RFC0020], it is possible to determine whether an octet
	   stream is UTF-8, UTF-16 (BE or LE), or UTF-32 (BE or LE) by looking
	   at the pattern of nulls in the first four octets.

			   00 00 00 xx  UTF-32BE
			   00 xx 00 xx  UTF-16BE
			   xx 00 00 00  UTF-32LE
			   xx 00 xx 00  UTF-16LE
			   xx xx xx xx  UTF-8
	'''
	assert(isinstance(json_bytes, bytes))
	if len(json_bytes) > 4:
		b1, b2, b3, b4 = json_bytes[0], json_bytes[1], json_bytes[2], json_bytes[3]
		if   b1 == 0 and b2 == 0 and b3 == 0 and b4 != 0:
			return "UTF-32BE"
		elif b1 == 0 and b2 != 0 and b3 == 0 and b4 != 0:
			return "UTF-16BE"
		elif b1 != 0 and b2 == 0 and b3 == 0 and b4 == 0:
			return "UTF-32LE"
		elif b1 != 0 and b2 == 0 and b3 != 0 and b4 == 0:
			return "UTF-16LE"
		elif b1 != 0 and b2 != 0 and b3 != 0 and b4 != 0:
			return "UTF-8"
		else:
			raise ValueError("Unknown encoding!")
	elif len(json_bytes) > 2:
		b1, b2 = json_bytes[0], json_bytes[1]
		if   b1 == 0 and b2 == 0:
			return "UTF-32BE"
		elif b1 == 0 and b2 != 0:
			return "UTF-16BE"
		elif b1 != 0 and b2 == 0:
			raise ValueError("Json string too short to definitively infer encoding.")
		elif b1 != 0 and b2 != 0:
			return "UTF-8"
		else:
			raise ValueError("Unknown encoding!")

	raise ValueError("Input string too short to guess encoding!")


class title_not_contains(object):
	""" An expectation for checking that the title *does not* contain a case-sensitive
	substring. title is the fragment of title expected
	returns True when the title matches, False otherwise
	"""
	def __init__(self, title):
		self.title = title


	def __call__(self, driver):
		return self.title not in driver.title

#pylint: disable-msg=E1101, C0325, R0201, W0702, W0703

def wait_for(condition_function):
	start_time = time.time()
	while time.time() < start_time + 3:
		if condition_function():
			return True
		else:
			time.sleep(0.1)
	raise Exception(
		'Timeout waiting for {}'.format(condition_function.__name__)
	)

class load_delay_context_manager(object):

	def __init__(self, browser):
		self.browser = browser

	def __enter__(self):
		self.old_page = self.browser.find_element_by_tag_name('html')

	def page_has_loaded(self):
		new_page = self.browser.find_element_by_tag_name('html')
		return new_page.id != self.old_page.id

	def __exit__(self, *_):
		wait_for(self.page_has_loaded)


class HeadRequest(urllib.request.Request):
	def get_method(self):
		# Apparently HEAD is now being blocked. Because douche.
		return "GET"
		# return "HEAD"

class HTTPRedirectBlockerErrorHandler(urllib.request.HTTPErrorProcessor):

	def http_response(self, request, response):
		code, msg, hdrs = response.code, response.msg, response.info()

		# only add this line to stop 302 redirection.
		if code == 302:
			print("Code!", 302)
			return response
		if code == 301:
			print("Code!", 301)
			return response

		print("[HTTPRedirectBlockerErrorHandler] http_response! code:", code)
		print(hdrs)
		print(msg)
		if not (200 <= code < 300):
			response = self.parent.error('http', request, response, code, msg, hdrs)
		return response

	https_response = http_response

# Custom redirect handler to work around
# issue https://bugs.python.org/issue17214
class HTTPRedirectHandler(urllib.request.HTTPRedirectHandler):
	# Implementation note: To avoid the server sending us into an
	# infinite loop, the request object needs to track what URLs we
	# have already seen.  Do this by adding a handler-specific
	# attribute to the Request object.
	def http_error_302(self, req, fp, code, msg, headers):
		# Some servers (incorrectly) return multiple Location headers
		# (so probably same goes for URI).  Use first header.
		if "location" in headers:
			newurl = headers["location"]
		elif "uri" in headers:
			newurl = headers["uri"]
		else:
			return

		# fix a possible malformed URL
		urlparts = urllib.parse.urlparse(newurl)

		# For security reasons we don't allow redirection to anything other
		# than http, https or ftp.

		if urlparts.scheme not in ('http', 'https', 'ftp', ''):
			raise urllib.error.HTTPError(
				newurl, code,
				"%s - Redirection to url '%s' is not allowed" % (msg, newurl),
				headers, fp)

		if not urlparts.path:
			urlparts = list(urlparts)
			urlparts[2] = "/"
		newurl = urllib.parse.urlunparse(urlparts)

		# http.client.parse_headers() decodes as ISO-8859-1.  Recover the
		# original bytes and percent-encode non-ASCII bytes, and any special
		# characters such as the space.
		newurl = urllib.parse.quote(
			newurl, encoding="iso-8859-1", safe=string.punctuation)
		newurl = urllib.parse.urljoin(req.full_url, newurl)

		# XXX Probably want to forget about the state of the current
		# request, although that might interact poorly with other
		# handlers that also use handler-specific request attributes
		new = self.redirect_request(req, fp, code, msg, headers, newurl)
		if new is None:
			return

		# loop detection
		# .redirect_dict has a key url if url was previously visited.
		if hasattr(req, 'redirect_dict'):
			visited = new.redirect_dict = req.redirect_dict
			if (visited.get(newurl, 0) >= self.max_repeats or
				len(visited) >= self.max_redirections):
				raise urllib.error.HTTPError(req.full_url, code,
								self.inf_msg + msg, headers, fp)
		else:
			visited = new.redirect_dict = req.redirect_dict = {}
		visited[newurl] = visited.get(newurl, 0) + 1

		# Don't close the fp until we are sure that we won't use it
		# with HTTPError.
		fp.read()
		fp.close()

		return self.parent.open(new, timeout=req.timeout)



# A urllib2 wrapper that provides error handling and logging, as well as cookie management. It's a bit crude, but it works.
# Also supports transport compresion.
# OOOOLLLLLLDDDDD, has lots of creaky internals. Needs some cleanup desperately, but lots of crap depends on almost everything.
# Arrrgh.

from threading import Lock
COOKIEWRITELOCK = Lock()

GLOBAL_COOKIE_FILE = None

class PreemptiveBasicAuthHandler(urllib.request.HTTPBasicAuthHandler):
	'''Preemptive basic auth.

	Instead of waiting for a 403 to then retry with the credentials,
	send the credentials if the url is handled by the password manager.
	Note: please use realm=None when calling add_password.'''
	def http_request(self, req):
		url = req.get_full_url()
		realm = None
		# this is very similar to the code from retry_http_basic_auth()
		# but returns a request object.
		user, pw = self.passwd.find_user_password(realm, url)
		if pw:
			raw = "%s:%s" % (user, pw)
			raw = raw.encode("ascii")
			auth = b'Basic ' + base64.standard_b64encode(raw).strip()
			req.add_unredirected_header(self.auth_header, auth)
		return req

	https_request = http_request

class WebGetRobust:
	COOKIEFILE = 'cookies.lwp'				# the path and filename to save your cookies in
	cj = None
	cookielib = None
	opener = None

	errorOutCount = 2
	# retryDelay = 0.1
	retryDelay = 0.0


	data = None

	# if test=true, no resources are actually fetched (for testing)
	# creds is a list of 3-tuples that gets inserted into the password manager.
	# it is structured [(top_level_url1, username1, password1), (top_level_url2, username2, password2)]
	def __init__(self, test=False, creds=None, logPath="Main.Web", cookie_lock=None, cloudflare=False, use_socks=False, alt_cookiejar=None):

		self.rules = {}
		self.rules['cloudflare'] = cloudflare
		if cookie_lock:
			self.cookie_lock = cookie_lock
		else:
			self.cookie_lock = COOKIEWRITELOCK

		self.pjs_driver = None
		self.cr_driver = None

		self.use_socks = use_socks

		# Override the global default socket timeout, so hung connections will actually time out properly.
		socket.setdefaulttimeout(15)

		self.log = logging.getLogger(logPath)
		# print("Webget init! Logpath = ", logPath)
		if creds:
			print("Have creds for a domain")
		if test:
			self.log.warning("-----------------------------------------------------------------------------------------------")
			self.log.warning("WARNING: WebGet in testing mode!")
			self.log.warning("-----------------------------------------------------------------------------------------------")

		# Due to general internet people douchebaggyness, I've basically said to hell with it and decided to spoof a whole assortment of browsers
		# It should keep people from blocking this scraper *too* easily
		self.browserHeaders = getUserAgent()

		self.testMode = test		# if we don't want to actually contact the remote server, you pass a string containing
									# pagecontent for testing purposes as test. It will get returned for any calls of getpage()

		self.data = urllib.parse.urlencode(self.browserHeaders)


		if creds:
			print("Have credentials, installing password manager into urllib handler.")
			passManager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
			for url, username, password in creds:
				passManager.add_password(None, url, username, password)
			self.credHandler = PreemptiveBasicAuthHandler(passManager)
		else:
			self.credHandler = None

		self.alt_cookiejar = alt_cookiejar
		self.loadCookies()

	def loadCookies(self):

		if self.alt_cookiejar is not None:
			self.alt_cookiejar.init_agent(new_headers=self.browserHeaders)
			self.cj = self.alt_cookiejar
		else:
			self.cj = http.cookiejar.LWPCookieJar()		# This is a subclass of FileCookieJar
												# that has useful load and save methods
		if self.cj is not None:
			if os.path.isfile(self.COOKIEFILE):
				try:
					self.cj.load(self.COOKIEFILE)
					# self.log.info("Loading CookieJar")
				except:
					self.log.critical("Cookie file is corrupt/damaged?")
					try:
						os.remove(self.COOKIEFILE)
					except FileNotFoundError:
						pass
			if http.cookiejar is not None:
				# self.log.info("Installing CookieJar")
				self.log.debug(self.cj)
				cookieHandler = urllib.request.HTTPCookieProcessor(self.cj)
				args = (cookieHandler, HTTPRedirectHandler)
				if self.credHandler:
					print("Have cred handler. Building opener using it")
					args += (self.credHandler, )
				if self.use_socks:
					print("Using Socks handler")
					args = (SocksiPyHandler(socks.SOCKS5, "127.0.0.1", 9050), ) + args

				self.opener = urllib.request.build_opener(*args)
				#self.opener.addheaders = [('User-Agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')]
				self.opener.addheaders = self.browserHeaders
				#urllib2.install_opener(self.opener)

		for cookie in self.cj:
			self.log.debug(cookie)
			#print cookie


	def chunkReport(self, bytesSoFar, totalSize):
		if totalSize:
			percent = float(bytesSoFar) / totalSize
			percent = round(percent * 100, 2)
			self.log.info("Downloaded %d of %d bytes (%0.2f%%)" % (bytesSoFar, totalSize, percent))
		else:
			self.log.info("Downloaded %d bytes" % (bytesSoFar))


	def chunkRead(self, response, chunkSize=2 ** 18, reportHook=None):
		contentLengthHeader = response.info().getheader('Content-Length')
		if contentLengthHeader:
			totalSize = contentLengthHeader.strip()
			totalSize = int(totalSize)
		else:
			totalSize = None
		bytesSoFar = 0
		pgContent = ""
		while 1:
			chunk = response.read(chunkSize)
			pgContent += chunk
			bytesSoFar += len(chunk)

			if not chunk:
				break

			if reportHook:
				reportHook(bytesSoFar, chunkSize, totalSize)

		return pgContent



	def getSoup(self, *args, **kwargs):
		if 'returnMultiple' in kwargs and kwargs['returnMultiple']:
			raise ValueError("getSoup cannot be called with 'returnMultiple' being true")

		if 'soup' in kwargs and kwargs['soup']:
			raise ValueError("getSoup contradicts the 'soup' directive!")

		page = self.getpage(*args, **kwargs)
		if isinstance(page, bytes):
			raise ValueError("Received content not decoded! Cannot parse!")

		soup = as_soup(page)
		return soup

	def getJson(self, *args, **kwargs):
		if 'returnMultiple' in kwargs and kwargs['returnMultiple']:
			raise ValueError("getSoup cannot be called with 'returnMultiple' being true")

		attempts = 0
		while 1:
			try:
				page = self.getpage(*args, **kwargs)
				if isinstance(page, bytes):
					page = page.decode(determine_json_encoding(page))
					# raise ValueError("Received content not decoded! Cannot parse!")

				page = page.strip()
				ret = json.loads(page)
				return ret
			except ValueError:
				if attempts < 1:
					attempts += 1
					self.log.error("JSON Parsing issue retreiving content from page!")
					for line in traceback.format_exc().split("\n"):
						self.log.error("%s", line.rstrip())
					self.log.error("Retrying!")

					# Scramble our current UA
					self.browserHeaders = getUserAgent()
					if self.alt_cookiejar:
						self.cj.init_agent(new_headers=self.browserHeaders)

					time.sleep(self.retryDelay)
				else:
					self.log.error("JSON Parsing issue, and retries exhausted!")
					# self.log.error("Page content:")
					# self.log.error(page)
					# with open("Error-ctnt-{}.json".format(time.time()), "w") as tmp_err_fp:
					# 	tmp_err_fp.write(page)
					raise

	def resetUa(self):

		if self.pjs_driver != None:
			self.pjs_driver.quit()
			self.pjs_driver = None

		if not self.pjs_driver:
			self._initPjsWebDriver()
		self._syncIntoPjsWebDriver()

		self.browserHeaders = getUserAgent()
		if self.alt_cookiejar:
			self.cj.init_agent(new_headers=self.browserHeaders)



	def getFileAndName(self, *args, **kwargs):
		if 'returnMultiple' in kwargs:
			raise ValueError("getFileAndName cannot be called with 'returnMultiple'")

		if 'soup' in kwargs and kwargs['soup']:
			raise ValueError("getFileAndName contradicts the 'soup' directive!")

		kwargs["returnMultiple"] = True

		pgctnt, pghandle = self.getpage(*args, **kwargs)

		info = pghandle.info()
		if not 'Content-Disposition' in info:
			hName = ''
		elif not 'filename=' in info['Content-Disposition']:
			hName = ''
		else:
			hName = info['Content-Disposition'].split('filename=')[1]
		return pgctnt, hName

	def buildRequest(self, pgreq, postData, addlHeaders, binaryForm, req_class = urllib.request.Request):
		# Encode Unicode URL's properly

		try:
			tmp = pgreq.encode("ascii")
		except UnicodeEncodeError:
			print("Wat?")
			print("pgreq: '%s'", pgreq)

		try:
			params = {}
			headers = {}
			if postData != None:
				self.log.info("Making a post-request! Params: '%s'", postData)
				params['data'] = urllib.parse.urlencode(postData).encode("utf-8")
			if addlHeaders != None:
				self.log.info("Have additional GET parameters!")
				for key, parameter in addlHeaders.items():
					self.log.info("	Item: '%s' -> '%s'", key, parameter)
				headers = addlHeaders
			if binaryForm:
				self.log.info("Binary form submission!")
				if 'data' in params:
					raise ValueError("You cannot make a binary form post and a plain post request at the same time!")

				params['data']            = binaryForm.make_result()
				headers['Content-type']   =  binaryForm.get_content_type()
				headers['Content-length'] =  len(params['data'])

			return req_class(pgreq, headers=headers, **params)

		except:
			self.log.critical("Invalid header or url")
			raise


	def decodeHtml(self, pageContent, cType):

		# this *should* probably be done using a parser.
		# However, it seems to be grossly overkill to shove the whole page (which can be quite large) through a parser just to pull out a tag that
		# should be right near the page beginning anyways.
		# As such, it's a regular expression for the moment

		# Regex is of bytes type, since we can't convert a string to unicode until we know the encoding the
		# bytes string is using, and we need the regex to get that encoding
		coding = re.search(rb"charset=[\'\"]?([a-zA-Z0-9\-]*)[\'\"]?", pageContent, flags=re.IGNORECASE)

		cType = b""
		charset = None
		try:
			if coding:
				cType = coding.group(1)
				codecs.lookup(cType.decode("ascii"))
				charset = cType.decode("ascii")

		except LookupError:

			# I'm actually not sure what I was thinking when I wrote this if statement. I don't think it'll ever trigger.
			if (b";" in cType) and (b"=" in cType): 		# the server is reporting an encoding. Now we use it to decode the

				dummy_docType, charset = cType.split(b";")
				charset = charset.split(b"=")[-1]

		if not charset:
			self.log.warning("Could not find encoding information on page - Using default charset. Shit may break!")
			charset = "iso-8859-1"

		try:
			pageContent = str(pageContent, charset)

		except UnicodeDecodeError:
			self.log.error("Encoding Error! Stripping invalid chars.")
			pageContent = pageContent.decode('utf-8', errors='ignore')

		return pageContent

	def decompressContent(self, coding, pgctnt):
		#preLen = len(pgctnt)
		if coding == 'deflate':
			compType = "deflate"

			pgctnt = zlib.decompress(pgctnt, -zlib.MAX_WBITS)

		elif coding == 'gzip':
			compType = "gzip"

			buf = io.BytesIO(pgctnt)
			f = gzip.GzipFile(fileobj=buf)
			pgctnt = f.read()

		elif coding == "sdch":
			raise ValueError("Wait, someone other then google actually supports SDCH compression?")

		else:
			compType = "none"

		return compType, pgctnt


	def getItem(self, itemUrl):

		try:
			content, handle = self.getpage(itemUrl, returnMultiple=True)
		except:
			print("Failure?")
			if self.rules['cloudflare']:
				if not self.stepThroughCloudFlare(itemUrl, titleNotContains='Just a moment...'):
					raise ValueError("Could not step through cloudflare!")
				# Cloudflare cookie set, retrieve again
				content, handle = self.getpage(itemUrl, returnMultiple=True)
			else:
				raise

		if not content or not handle:
			raise urllib.error.URLError("Failed to retreive file from page '%s'!" % itemUrl)

		fileN = urllib.parse.unquote(urllib.parse.urlparse(handle.geturl())[2].split("/")[-1])
		fileN = bs4.UnicodeDammit(fileN).unicode_markup
		mType = handle.info()['Content-Type']

		# If there is an encoding in the content-type (or any other info), strip it out.
		# We don't care about the encoding, since WebFunctions will already have handled that,
		# and returned a decoded unicode object.
		if mType and ";" in mType:
			mType = mType.split(";")[0].strip()

		# *sigh*. So minus.com is fucking up their http headers, and apparently urlencoding the
		# mime type, because apparently they're shit at things.
		# Anyways, fix that.
		if '%2F' in  mType:
			mType = mType.replace('%2F', '/')

		self.log.info("Retreived file of type '%s', name of '%s' with a size of %0.3f K", mType, fileN, len(content)/1000.0)
		return content, fileN, mType


	def _initPjsWebDriver(self):
		if self.pjs_driver:
			self.pjs_driver.quit()
		dcap = dict(DesiredCapabilities.PHANTOMJS)
		wgSettings = dict(self.browserHeaders)
		# Install the headers from the WebGet class into phantomjs
		dcap["phantomjs.page.settings.userAgent"] = wgSettings.pop('User-Agent')
		for headerName in wgSettings:
			if headerName != 'Accept-Encoding':
				dcap['phantomjs.page.customHeaders.{header}'.format(header=headerName)] = wgSettings[headerName]

		self.pjs_driver = selenium.webdriver.PhantomJS(desired_capabilities=dcap)
		self.pjs_driver.set_window_size(1280, 1024)

	def _initCrWebDriver(self):
		if self.cr_driver:
			self.cr_driver.quit()
		dcap = dict(DesiredCapabilities.CHROME)
		wgSettings = dict(self.browserHeaders)
		# Install the headers from the WebGet class into phantomjs
		user_agent = wgSettings.pop('User-Agent')
		dcap["chrome.page.settings.userAgent"] = user_agent
		for headerName in wgSettings:
			if headerName != 'Accept-Encoding':
				dcap['chrome.page.customHeaders.{header}'.format(header=headerName)] = wgSettings[headerName]

		dcap["chrome.switches"] = ["--user-agent="+user_agent]


		chromedriver = r'./venv/bin/chromedriver'
		chrome       = r'./Headless/headless_shell'

		chrome_options = selenium.webdriver.chrome.options.Options()
		chrome_options.binary_location = chrome
		chrome_options.add_argument('--load-component-extension')
		chrome_options.add_argument("--user-agent=\"{}\"".format(user_agent))
		chrome_options.add_argument('--verbose')
		chrome_options.add_argument('--no-sandbox')
		chrome_options.add_argument('--disable-extension')

		self.cr_driver = selenium.webdriver.Chrome(chrome_options=chrome_options, desired_capabilities=dcap)
		# We can't set the chrome desired capabilities, since headless chrome
		# doesn't allow extensions.

		self.cr_driver.set_page_load_timeout(30)

	def _syncIntoPjsWebDriver(self):
		# TODO
		pass

	def _syncOutOfPjsWebDriver(self):
		for cookie in self.pjs_driver.get_cookies():
			self.addSeleniumCookie(cookie)


	def getItemPhantomJS(self, itemUrl):
		self.log.info("Fetching page for URL: '%s' with PhantomJS" % itemUrl)

		if not self.pjs_driver:
			self._initPjsWebDriver()
		self._syncIntoPjsWebDriver()

		with load_delay_context_manager(self.pjs_driver):
			self.pjs_driver.get(itemUrl)
		time.sleep(3)

		fileN = urllib.parse.unquote(urllib.parse.urlparse(self.pjs_driver.current_url)[2].split("/")[-1])
		fileN = bs4.UnicodeDammit(fileN).unicode_markup

		self._syncOutOfPjsWebDriver()

		# Probably a bad assumption
		mType = "text/html"

		# So, self.pjs_driver.page_source appears to be the *compressed* page source as-rendered. Because reasons.
		source = self.pjs_driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")

		assert source != '<head></head><body></body>'

		source = "<html>"+source+"</html>"
		return source, fileN, mType


	def decodeTextContent(self, pgctnt, cType):

		if cType:
			if (";" in cType) and ("=" in cType):
				# the server is reporting an encoding. Now we use it to decode the content
				# Some wierdos put two charsets in their headers:
				# `text/html;Charset=UTF-8;charset=UTF-8`
				# Split, and take the first two entries.
				docType, charset = cType.split(";")[:2]
				charset = charset.split("=")[-1]

				# Only decode content marked as text (yeah, google is serving zip files
				# with the content-disposition charset header specifying "UTF-8") or
				# specifically allowed other content types I know are really text.
				decode = ['application/atom+xml', 'application/xml', "application/json", 'text']
				if any([item in docType for item in decode]):
					try:
						pgctnt = str(pgctnt, charset)
					except UnicodeDecodeError:
						self.log.error("Encoding Error! Stripping invalid chars.")
						pgctnt = pgctnt.decode('utf-8', errors='ignore')

			else:
				# The server is not reporting an encoding in the headers.
				# Use content-aware mechanisms for determing the content encoding.


				if "text/html" in cType or \
					'text/javascript' in cType or    \
					'text/css' in cType or    \
					'application/xml' in cType or    \
					'application/atom+xml' in cType:				# If this is a html/text page, we want to decode it using the local encoding

					pgctnt = self.decodeHtml(pgctnt, cType)

				elif "text/plain" in cType or "text/xml" in cType:
					pgctnt = bs4.UnicodeDammit(pgctnt).unicode_markup

				# Assume JSON is utf-8. Probably a bad idea?
				elif "application/json" in cType:
					pgctnt = pgctnt.decode('utf-8')

				elif "text" in cType:
					self.log.critical("Unknown content type!")
					self.log.critical(cType)

		else:
			self.log.critical("No content disposition header!")
			self.log.critical("Cannot guess content type!")

		return pgctnt

	def retreiveContent(self, pgreq, pghandle, callBack):
		try:
			# If we have a progress callback, call it for chunked read.
			# Otherwise, just read in the entire content.
			if callBack:
				pgctnt = self.chunkRead(pghandle, 2 ** 17, reportHook=callBack)
			else:
				pgctnt = pghandle.read()


			if pgctnt == None:
				return False

			self.log.info("URL fully retrieved.")

			preDecompSize = len(pgctnt)/1000.0

			encoded = pghandle.headers.get('Content-Encoding')
			compType, pgctnt = self.decompressContent(encoded, pgctnt)


			decompSize = len(pgctnt)/1000.0
			# self.log.info("Page content type = %s", type(pgctnt))
			cType = pghandle.headers.get("Content-Type")
			if compType == 'none':
				self.log.info("Compression type = %s. Content Size = %0.3fK. File type: %s.", compType, decompSize, cType)
			else:
				self.log.info("Compression type = %s. Content Size compressed = %0.3fK. Decompressed = %0.3fK. File type: %s.", compType, preDecompSize, decompSize, cType)

			pgctnt = self.decodeTextContent(pgctnt, cType)

			return pgctnt

		except:
			print("pghandle = ", pghandle)

			self.log.error(sys.exc_info())
			traceback.print_exc()
			self.log.error("Error Retrieving Page! - Transfer failed. Waiting %s seconds before retrying", self.retryDelay)

			try:
				self.log.critical("Critical Failure to retrieve page! %s at %s", pgreq.get_full_url(), time.ctime(time.time()))
				self.log.critical("Exiting")
			except:
				self.log.critical("And the URL could not be printed due to an encoding error")
			print()
			self.log.error(pghandle)
			time.sleep(self.retryDelay)

		return False


		# HUGE GOD-FUNCTION.
		# OH GOD FIXME.

		# postData expects a dict
		# addlHeaders also expects a dict
	def getpage(self, requestedUrl, **kwargs):
		# pgreq = fixurl(pgreq)

		# strip trailing and leading spaces.
		requestedUrl = requestedUrl.strip()

		# addlHeaders = None, returnMultiple = False, callBack=None, postData=None, soup=False, retryQuantity=None, nativeError=False, binaryForm=False

		# If we have 'soup' as a param, just pop it, and call `getSoup()`.
		if 'soup' in kwargs and kwargs['soup']:
			self.log.warn("'soup' kwarg is depreciated. Please use the `getSoup()` call instead.")
			kwargs.pop('soup')

			return self.getSoup(requestedUrl, **kwargs)

		# Decode the kwargs values
		addlHeaders    = kwargs.setdefault("addlHeaders",     None)
		returnMultiple = kwargs.setdefault("returnMultiple",  False)
		callBack       = kwargs.setdefault("callBack",        None)
		postData       = kwargs.setdefault("postData",        None)
		retryQuantity  = kwargs.setdefault("retryQuantity",   None)
		nativeError    = kwargs.setdefault("nativeError",     False)
		binaryForm     = kwargs.setdefault("binaryForm",      False)

		# Conditionally encode the referrer if needed, because otherwise
		# urllib will barf on unicode referrer values.
		if addlHeaders and 'Referer' in addlHeaders:
			addlHeaders['Referer'] = iri2uri(addlHeaders['Referer'])

		requestedUrl = iri2uri(requestedUrl)


		if not self.testMode:
			retryCount = 0
			while 1:

				pgctnt = None
				pghandle = None

				pgreq = self.buildRequest(requestedUrl, postData, addlHeaders, binaryForm)

				errored = False
				lastErr = ""

				retryCount = retryCount + 1

				if (retryQuantity and retryCount > retryQuantity) or (not retryQuantity and retryCount > self.errorOutCount):
					self.log.error("Failed to retrieve Website : %s at %s All Attempts Exhausted", pgreq.get_full_url(), time.ctime(time.time()))
					pgctnt = None
					try:
						self.log.critical("Critical Failure to retrieve page! %s at %s, attempt %s", pgreq.get_full_url(), time.ctime(time.time()), retryCount)
						self.log.critical("Error: %s", lastErr)
						self.log.critical("Exiting")
					except:
						self.log.critical("And the URL could not be printed due to an encoding error")
					break

				#print "execution", retryCount
				try:
					# print("Getpage!", requestedUrl, kwargs)
					pghandle = self.opener.open(pgreq, timeout=30)					# Get Webpage
					# print("Gotpage")

				except urllib.error.HTTPError as e:								# Lotta logging
					self.log.warning("Error opening page: %s at %s On Attempt %s.", pgreq.get_full_url(), time.ctime(time.time()), retryCount)
					self.log.warning("Error Code: %s", e)

					#traceback.print_exc()
					lastErr = e
					try:

						self.log.warning("Original URL: %s", requestedUrl)
						errored = True
					except:
						self.log.warning("And the URL could not be printed due to an encoding error")

					if e.code == 404:
						#print "Unrecoverable - Page not found. Breaking"
						self.log.critical("Unrecoverable - Page not found. Breaking")
						break

					time.sleep(self.retryDelay)
					if e.code == 503:
						errcontent = e.read()
						if b'This process is automatic. Your browser will redirect to your requested content shortly.' in errcontent:
							self.log.warn("Cloudflare failure! Doing automatic step-through.")
							self.stepThroughCloudFlare(requestedUrl, titleNotContains="Just a moment...")
				except UnicodeEncodeError:
					self.log.critical("Unrecoverable Unicode issue retreiving page - %s", requestedUrl)
					for line in traceback.format_exc().split("\n"):
						self.log.critical("%s", line.rstrip())
					self.log.critical("Parameters:")
					self.log.critical("	requestedUrl: '%s'", requestedUrl)
					self.log.critical("	postData:     '%s'", postData)
					self.log.critical("	addlHeaders:  '%s'", addlHeaders)
					self.log.critical("	binaryForm:   '%s'", binaryForm)


					break





				except Exception:
					errored = True
					#traceback.print_exc()
					lastErr = sys.exc_info()
					self.log.warning("Retreival failed. Traceback:")
					self.log.warning(lastErr)
					self.log.warning(traceback.format_exc())

					self.log.warning("Error Retrieving Page! - Trying again - Waiting %s seconds", self.retryDelay)

					try:
						self.log.critical("Error on page - %s", requestedUrl)
					except:
						self.log.critical("And the URL could not be printed due to an encoding error")

					time.sleep(self.retryDelay)


					continue

				if pghandle != None:
					self.log.info("Request for URL: %s succeeded at %s On Attempt %s. Recieving...", pgreq.get_full_url(), time.ctime(time.time()), retryCount)
					pgctnt = self.retreiveContent(pgreq, pghandle, callBack)

					# if retreiveContent did not return false, it managed to fetch valid results, so break
					if pgctnt != False:
						break

		if errored and pghandle != None:
			print(("Later attempt succeeded %s" % pgreq.get_full_url()))
			#print len(pgctnt)
		elif errored and pghandle == None:

			if lastErr and nativeError:
				raise lastErr
			raise urllib.error.URLError("Failed to retreive page '%s'!" % (requestedUrl, ))

		if returnMultiple:
			return pgctnt, pghandle
		else:
			if pghandle:
				pghandle.close()
			return pgctnt

	def getHead(self, url, addlHeaders):
		for x in range(9999):
			try:
				self.log.info("Doing HTTP HEAD request for '%s'", url)
				pgreq = self.buildRequest(url, None, addlHeaders, None, req_class=HeadRequest)
				pghandle = self.opener.open(pgreq, timeout=30)
				returl = pghandle.geturl()
				if returl != url:
					self.log.info("HEAD request returned a different URL '%s'", returl)

				return returl
			except socket.timeout as e:
				self.log.info("Timeout, retrying....")
				if x >= 3:
					self.log.error("Failure fetching: %s", url)
					raise e
			except urllib.error.URLError as e:
				# Continue even in the face of cloudflare crapping it's pants
				if e.code == 500 and e.geturl():
					return e.geturl()
				self.log.info("URLError, retrying....")
				if x >= 3:
					self.log.error("Failure fetching: %s", url)
					raise e

	def getHeadTitlePhantomJS(self, url, referrer):
		self.getHeadPhantomJS(url, referrer)
		ret = {
			'url'   : self.pjs_driver.current_url,
			'title' : self.pjs_driver.title,
		}
		return ret

	def getHeadPhantomJS(self, url, referrer):
		self.log.info("Getting HEAD with PhantomJS")

		if not self.pjs_driver:
			self._initPjsWebDriver()
		self._syncIntoPjsWebDriver()

		def try_get(loc_url):
			tries = 3
			for x in range(9999):
				try:
					self.pjs_driver.get(loc_url)
					time.sleep(random.uniform(2, 6))
					return
				except socket.timeout as e:
					if x > tries:
						raise e

		try_get(referrer)
		try_get(url)

		self._syncOutOfPjsWebDriver()

		return self.pjs_driver.current_url

	def syncCookiesFromFile(self):
		# self.log.info("Synchronizing cookies with cookieFile.")
		if os.path.isfile(self.COOKIEFILE):
			self.cj.save("cookietemp.lwp")
			self.cj.load(self.COOKIEFILE)
			self.cj.load("cookietemp.lwp")
		# First, load any changed cookies so we don't overwrite them
		# However, we want to persist any cookies that we have that are more recent then the saved cookies, so we temporarily save
		# the cookies in memory to a temp-file, then load the cookiefile, and finally overwrite the loaded cookies with the ones from the
		# temp file

	def updateCookiesFromFile(self):
		if os.path.exists(self.COOKIEFILE):
			# self.log.info("Synchronizing cookies with cookieFile.")
			self.cj.load(self.COOKIEFILE)
		# Update cookies from cookiefile

	def addCookie(self, inCookie):
		self.log.info("Updating cookie!")
		self.cj.set_cookie(inCookie)

	def addSeleniumCookie(self, cookieDict):
		'''
		Install a cookie exported from a selenium webdriver into
		the active opener
		'''
		# print cookieDict
		cookie = http.cookiejar.Cookie(
				version            = 0,
				name               = cookieDict['name'],
				value              = cookieDict['value'],
				port               = None,
				port_specified     = False,
				domain             = cookieDict['domain'],
				domain_specified   = True,
				domain_initial_dot = False,
				path               = cookieDict['path'],
				path_specified     = False,
				secure             = cookieDict['secure'],
				expires            = cookieDict['expiry'] if 'expiry' in cookieDict else None,
				discard            = False,
				comment            = None,
				comment_url        = None,
				rest               = {"httponly":"%s" % cookieDict['httponly']},
				rfc2109            = False
			)

		self.cj.set_cookie(cookie)

	def initLogging(self):
		print("WARNING - Webget logging re-initialized?")
		mainLogger = logging.getLogger("Main")			# Main logger
		mainLogger.setLevel(logging.DEBUG)

		ch = logging.StreamHandler(sys.stdout)
		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		ch.setFormatter(formatter)
		mainLogger.addHandler(ch)

	def saveCookies(self, halting=False):

		locked = self.cookie_lock.acquire(timeout=5)
		if not locked:
			self.log.error("Failed to acquire cookie-lock!")
			return

		# print("Have %d cookies before saving cookiejar" % len(self.cj))
		try:
			# self.log.info("Trying to save cookies!")
			if self.cj is not None:							# If cookies were used

				self.syncCookiesFromFile()

				# self.log.info("Have cookies to save")
				for cookie in self.cj:
					# print(cookie)
					# print(cookie.expires)

					if isinstance(cookie.expires, int) and cookie.expires > 30000000000:		# Clamp cookies that expire stupidly far in the future because people are assholes
						cookie.expires = 30000000000

				# self.log.info("Calling save function")
				self.cj.save(self.COOKIEFILE)					# save the cookies again


				# self.log.info("Cookies Saved")
			else:
				self.log.info("No cookies to save?")
		except Exception as e:
			pass
			# The destructor call order is too incoherent, and shit fails
			# during the teardown with null-references. The error printout is
			# not informative, so just silence it.
			# print("Possible error on exit (or just the destructor): '%s'." % e)
		finally:
			self.cookie_lock.release()

		# print("Have %d cookies after saving cookiejar" % len(self.cj))
		if not halting:
			self.syncCookiesFromFile()
		# print "Have %d cookies after reloading cookiejar" % len(self.cj)

	def getCookies(self):

		locked = self.cookie_lock.acquire(timeout=5)
		if not locked:
			raise RuntimeError("Could not acquire lock on cookiejar")

		try:
			# self.log.info("Trying to save cookies!")
			if self.cj is not None:							# If cookies were used
				self.syncCookiesFromFile()
		finally:
			self.cookie_lock.release()

		return self.cj


	def __del__(self):
		# print "WGH Destructor called!"
		self.saveCookies(halting=True)

		if self.pjs_driver != None:
			self.pjs_driver.quit()


	def stepThroughCloudFlare(self, url, titleContains='', titleNotContains=''):
		'''
		Use Selenium+PhantomJS to access a resource behind cloudflare protection.

		Params:
			``url`` - The URL to access that is protected by cloudflare
			``titleContains`` - A string that is in the title of the protected page, and NOT the
				cloudflare intermediate page. The presence of this string in the page title
				is used to determine whether the cloudflare protection has been successfully
				penetrated.

		The current WebGetRobust headers are installed into the selenium browser, which
		is then used to access the protected resource.

		Once the protected page has properly loaded, the cloudflare access cookie is
		then extracted from the selenium browser, and installed back into the WebGetRobust
		instance, so it can continue to use the cloudflare auth in normal requests.

		'''

		if (not titleContains) and (not titleNotContains):
			raise ValueError("You must pass either a string the title should contain, or a string the title shouldn't contain!")

		if titleContains and titleNotContains:
			raise ValueError("You can only pass a single conditional statement!")


		self.log.info("Attempting to access page through cloudflare browser verification.")

		dcap = dict(DesiredCapabilities.PHANTOMJS)
		wgSettings = dict(self.browserHeaders)

		# Install the headers from the WebGet class into phantomjs
		dcap["phantomjs.page.settings.userAgent"] = wgSettings.pop('User-Agent')
		for headerName in wgSettings:
			dcap['phantomjs.page.customHeaders.{header}'.format(header=headerName)] = wgSettings[headerName]

		driver = selenium.webdriver.PhantomJS(desired_capabilities=dcap)
		driver.set_window_size(1024, 768)

		driver.get(url)

		if titleContains:
			condition = EC.title_contains(titleContains)
		elif titleNotContains:
			condition = title_not_contains(titleNotContains)
		else:
			raise ValueError("Wat?")


		try:
			WebDriverWait(driver, 20).until(condition)
			success = True
			self.log.info("Successfully accessed main page!")
		except TimeoutException:
			self.log.error("Could not pass through cloudflare blocking!")
			success = False
		# Add cookies to cookiejar

		for cookie in driver.get_cookies():
			self.addSeleniumCookie(cookie)
			#print cookie[u"value"]

		self.syncCookiesFromFile()

		return success




# Convert an IRI to a URI following the rules in RFC 3987
#
# The characters we need to enocde and escape are defined in the spec:
#
# iprivate =  %xE000-F8FF / %xF0000-FFFFD / %x100000-10FFFD
# ucschar = %xA0-D7FF / %xF900-FDCF / %xFDF0-FFEF
#         / %x10000-1FFFD / %x20000-2FFFD / %x30000-3FFFD
#         / %x40000-4FFFD / %x50000-5FFFD / %x60000-6FFFD
#         / %x70000-7FFFD / %x80000-8FFFD / %x90000-9FFFD
#         / %xA0000-AFFFD / %xB0000-BFFFD / %xC0000-CFFFD
#         / %xD0000-DFFFD / %xE1000-EFFFD

escape_range = [
	(0xA0, 0xD7FF),
	(0xE000, 0xF8FF),
	(0xF900, 0xFDCF),
	(0xFDF0, 0xFFEF),
	(0x10000, 0x1FFFD),
	(0x20000, 0x2FFFD),
	(0x30000, 0x3FFFD),
	(0x40000, 0x4FFFD),
	(0x50000, 0x5FFFD),
	(0x60000, 0x6FFFD),
	(0x70000, 0x7FFFD),
	(0x80000, 0x8FFFD),
	(0x90000, 0x9FFFD),
	(0xA0000, 0xAFFFD),
	(0xB0000, 0xBFFFD),
	(0xC0000, 0xCFFFD),
	(0xD0000, 0xDFFFD),
	(0xE1000, 0xEFFFD),
	(0xF0000, 0xFFFFD),
	(0x100000, 0x10FFFD),
]

def encode(c):
	retval = c
	i = ord(c)
	for low, high in escape_range:
		if i < low:
			break
		if i >= low and i <= high:
			retval = "".join(["%%%2X" % o for o in c.encode('utf-8')])
			break
	return retval


def iri2uri(uri):
	"""Convert an IRI to a URI. Note that IRIs must be
	passed in a unicode strings. That is, do not utf-8 encode
	the IRI before passing it into the function."""

	assert uri != None, 'iri2uri must be passed a non-none string!'

	original = uri
	if isinstance(uri ,str):
		(scheme, authority, path, query, fragment) = urllib.parse.urlsplit(uri)
		authority = authority.encode('idna').decode('utf-8')
		# For each character in 'ucschar' or 'iprivate'
		#  1. encode as utf-8
		#  2. then %-encode each octet of that utf-8
		path = urllib.parse.quote(path)
		uri = urllib.parse.urlunsplit((scheme, authority, path, query, fragment))
		uri = "".join([encode(c) for c in uri])

	# urllib.parse.urlunsplit(urllib.parse.urlsplit({something})
	# strips any trailing "?" chars. While this may be legal according to the
	# spec, it breaks some services. Therefore, we patch
	# the "?" back in if it has been removed.
	if original.endswith("?") and not uri.endswith("?"):
		uri = uri+"?"
	return uri


class DummyLog:									# For testing WebGetRobust (mostly)
	logText = ""

	def __init__(self):
		pass

	def __repr__(self):
		return self.logText

	def write(self, string):
		self.logText = "%s\n%s" % (self.logText, string)

	def close(self):
		pass




# Due to general internet people douchebaggyness, I've basically said to hell with it and decided to spoof a whole assortment of browsers
# It should keep people from blocking this scraper *too* easily

# This file generates a random browser user-agent, It should have an extremely large set of possible UA structures.
USER_AGENTS = [

	'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/8.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; BIDUBrowser 2.x)',
	'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)',
	'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 1.0.3705; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
	'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.2; WOW64; Trident/7.0; .NET4.0E; .NET4.0C; Media Center PC 6.0; .NET CLR 3.5.30729; .NET CLR 2.0.50727; .NET CLR 3.0.30729; InfoPath.3; ms-office; MSOffice 15)',
	'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1)',
	'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)',
	'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1; 125LA; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022)',
	'Mozilla/4.0 (compatible;)',
	'Mozilla/5.0',
	'Mozilla/5.0 (BB10; Kbd) AppleWebKit/537.35+ (KHTML, like Gecko) Version/10.3.2.2876 Mobile Safari/537.35+',
	'Mozilla/5.0 (compatible) Feedfetcher-Google; (+http://www.google.com/feedfetcher.html)',
	'Mozilla/5.0 (compatible; AhrefsBot/5.2; +http://ahrefs.com/robot/)',
	'Mozilla/5.0 (compatible; archive.org_bot +http://www.archive.org/details/archive.org_bot)',
	'Mozilla/5.0 (compatible; archive.org_bot; Wayback Machine Live Record; +http://archive.org/details/archive.org_bot)',
	'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
	'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)',
	'Mozilla/5.0 (compatible; coccocbot-web/1.0; +http://help.coccoc.com/searchengine)',
	'Mozilla/5.0 (compatible; Discordbot/2.0; +https://discordapp.com)',
	'Mozilla/5.0 (compatible; DotBot/1.1; http://www.opensiteexplorer.org/dotbot, help@moz.com)',
	'Mozilla/5.0 (compatible; DuckDuckGo-Favicons-Bot/1.0; +http://duckduckgo.com)',
	'Mozilla/5.0 (compatible; evc-batch/2.0.20170913102128)',
	'Mozilla/5.0 (compatible; Exabot/3.0; +http://www.exabot.com/go/robot)',
	'Mozilla/5.0 (compatible; FLinkhubbot/1.1; +hello@flinkhub.com )',
	'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
	'Mozilla/5.0 (compatible; linkdexbot/2.2; +http://www.linkdex.com/bots/)',
	'Mozilla/5.0 (compatible; Linux x86_64; Mail.RU_Bot/2.0; +http://go.mail.ru/help/robots)',
	'Mozilla/5.0 (compatible; MJ12bot/v1.4.7; http://mj12bot.com/)',
	'Mozilla/5.0 (compatible; MJ12bot/v1.4.8; http://mj12bot.com/)',
	'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
	'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0; MASBJS)',
	'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; Trident/5.0)',
	'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; Trident/5.0)',
	'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
	'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; NOKIA; Lumia 900)',
	'Mozilla/5.0 (compatible; Nmap Scripting Engine; https://nmap.org/book/nse.html)',
	'Mozilla/5.0 (compatible; Pinterestbot/1.0; +http://www.pinterest.com/bot.html)',
	'Mozilla/5.0 (compatible; SemrushBot-BA; +http://www.semrush.com/bot.html)',
	'Mozilla/5.0 (compatible; SemrushBot/1.2~bl; +http://www.semrush.com/bot.html)',
	'Mozilla/5.0 (compatible; SeznamBot/3.2; +http://napoveda.seznam.cz/en/seznambot-intro/)',
	'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
	'Mozilla/5.0 (compatible; YandexAccessibilityBot/3.0; +http://yandex.com/bots)',
	'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
	'Mozilla/5.0 (compatible; YandexImages/3.0; +http://yandex.com/bots)',
	'Mozilla/5.0 (iPad; CPU OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A403 Safari/602.1',
	'Mozilla/5.0 (iPad; CPU OS 10_1_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/61.0.3163.73 Mobile/14B100 Safari/602.1',
	'Mozilla/5.0 (iPad; CPU OS 10_1_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0 Mobile/14B100 Safari/602.1',
	'Mozilla/5.0 (iPad; CPU OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0 Mobile/14C92 Safari/602.1',
	'Mozilla/5.0 (iPad; CPU OS 10_2_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/60.0.3112.89 Mobile/14D27 Safari/602.1',
	'Mozilla/5.0 (iPad; CPU OS 10_2_1 like Mac OS X) AppleWebKit/602.4.6 (KHTML, like Gecko) Version/10.0 Mobile/14D27 Safari/602.1',
	'Mozilla/5.0 (iPad; CPU OS 10_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E277 Safari/602.1',
	'Mozilla/5.0 (iPad; CPU OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
	'Mozilla/5.0 (iPad; CPU OS 10_3_2 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) CriOS/60.0.3112.89 Mobile/14F89 Safari/602.1',
	'Mozilla/5.0 (iPad; CPU OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.0 Mobile/14F89 Safari/602.1',
	'Mozilla/5.0 (iPad; CPU OS 10_3_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) GSA/34.1.167176684 Mobile/14G60 Safari/602.1',
	'Mozilla/5.0 (iPad; CPU OS 10_3_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) CriOS/60.0.3112.89 Mobile/14G60 Safari/602.1',
	'Mozilla/5.0 (iPad; CPU OS 10_3_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) CriOS/61.0.3163.73 Mobile/14G60 Safari/602.1',
	'Mozilla/5.0 (iPad; CPU OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.0 Mobile/14G60 Safari/602.1',
	'Mozilla/5.0 (iPad; CPU OS 5_1_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B206 Safari/7534.48.3',
	'Mozilla/5.0 (iPad; CPU OS 7_1_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D201 Safari/9537.53',
	'Mozilla/5.0 (iPad; CPU OS 8_1_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B440 Safari/600.1.4',
	'Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
	'Mozilla/5.0 (iPad; CPU OS 9_3_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13G34 Safari/601.1',
	'Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/60.0.3112.89 Mobile/13G36 Safari/601.1.46',
	'Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/61.0.3163.73 Mobile/13G36 Safari/601.1.46',
	'Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13G36 Safari/601.1',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:44.0) Gecko/20100101 Firefox/44.0',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:55.0) Gecko/20100101 Firefox/55.0',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:55.0) Gecko/20100101 Firefox/55.0',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:53.0) Gecko/20100101 Firefox/53.0',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:54.0) Gecko/20100101 Firefox/54.0',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:48.0) Gecko/20100101 Firefox/48.0',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:48.0) Gecko/20100101 Firefox/48.0',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:55.0) Gecko/20100101 Firefox/55.0',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/601.6.17 (KHTML, like Gecko) Version/9.1.1 Safari/601.6.17',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2752.0 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.8 (KHTML, like Gecko) Version/9.1.3 Safari/601.7.8',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/603.2.5 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.5',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/603.1.30 (KHTML, like Gecko)',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko)',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_5_8) AppleWebKit/534.50.2 (KHTML, like Gecko) Version/5.0.6 Safari/533.22.3',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/6.1.3 Safari/537.75.14',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/601.7.8 (KHTML, like Gecko) Version/9.1.3 Safari/537.86.7',
	'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586',
	'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.105 Safari/537.36 Vivaldi/1.92.917.43',
	'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; rv:55.0) Gecko/20100101 Firefox/55.0',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063,gzip(gfe)',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36 OPR/47.0.2631.71',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36 OPR/47.0.2631.80',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.18 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3214.0 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
	'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/7.0.6.1042 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2700.0 Iron Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.0.12195 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.0.12195 Safari/537.36,gzip(gfe)',
	'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.11.2987.98 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.13.2987.98 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.2988.0 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.1.3029.81 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36 Vivaldi/1.91.867.42',
	'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 YaBrowser/17.7.1.791 Yowser/2.5 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.105 Safari/537.36 Vivaldi/1.92.917.43',
	'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 YaBrowser/17.9.1.449 (beta) Yowser/2.5 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36 OPR/47.0.2631.55',
	'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36 OPR/47.0.2631.71',
	'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36 OPR/47.0.2631.80',
	'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36 OPR/47.0.2631.80 (Edition Campaign 34)',
	'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.71 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) coc_coc_browser/61.4.120 Chrome/55.4.2883.120 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) coc_coc_browser/66.4.102 Chrome/60.4.3112.102 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) coc_coc_browser/66.4.104 Chrome/60.4.3112.104 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/5.0.4.3000 Chrome/47.0.2526.73 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0',
	'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
	'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
	'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
	'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
	'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0',
	'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0,gzip(gfe)',
	'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; MATBJS; rv:11.0) like Gecko',
	'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
	'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.12 Safari/537.36',
	'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36',
	'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
	'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36,gzip(gfe)',
	'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 YaBrowser/17.3.0.1785 Yowser/2.5 Safari/537.36',
	'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) coc_coc_browser/50.2.163 Chrome/44.2.2403.163 Safari/537.36',
	'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) coc_coc_browser/56.3.154 Chrome/50.3.2661.154 Safari/537.36',
	'Mozilla/5.0 (Windows NT 5.1; rv:11.0) Gecko Firefox/11.0 (via ggpht.com GoogleImageProxy)',
	'Mozilla/5.0 (Windows NT 5.1; rv:25.0) Gecko/20100101 Firefox/25.0',
	'Mozilla/5.0 (Windows NT 5.1; rv:30.0) Gecko/20100101 Firefox/30.0',
	'Mozilla/5.0 (Windows NT 5.1; rv:43.0) Gecko/20100101 Firefox/43.0',
	'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
	'Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0',
	'Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0,gzip(gfe)',
	'Mozilla/5.0 (Windows NT 5.1; rv:6.0.2) Gecko/20100101 Firefox/6.0.2',
	'Mozilla/5.0 (Windows NT 5.2; rv:52.0) Gecko/20100101 Firefox/52.0',
	'Mozilla/5.0 (Windows NT 6.0; rv:22.0) Gecko/20130405 Firefox/22.0',
	'Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36,gzip(gfe)',
	'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/7.0.6.1042 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.273 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.1.3029.81 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 YaBrowser/17.7.1.791 Yowser/2.5 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36,gzip(gfe)',
	'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36 OPR/47.0.2631.71',
	'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36,gzip(gfe)',
	'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) coc_coc_browser/66.4.104 Chrome/60.4.3112.104 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.9.5.1000 Chrome/39.0.2146.0 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; rv:38.0) Gecko/20100101 Firefox/38.0',
	'Mozilla/5.0 (Windows NT 6.1; rv:38.9) Gecko/20100101 Goanna/2.2 Firefox/38.9 PaleMoon/26.5.0',
	'Mozilla/5.0 (Windows NT 6.1; rv:42.0) Gecko/20100101 Firefox/42.0',
	'Mozilla/5.0 (Windows NT 6.1; rv:47.0) Gecko/20100101 Firefox/47.0',
	'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0',
	'Mozilla/5.0 (Windows NT 6.1; rv:55.0) Gecko/20100101 Firefox/55.0',
	'Mozilla/5.0 (Windows NT 6.1; rv:55.0) Gecko/20100101 Firefox/55.0,gzip(gfe)',
	'Mozilla/5.0 (Windows NT 6.1; rv:56.0) Gecko/20100101 Firefox/56.0',
	'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
	'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.85 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2540.0 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36 OPR/44.0.2510.1449',
	'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36 OPR/47.0.2631.55',
	'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36 OPR/47.0.2631.71',
	'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36 OPR/47.0.2631.80',
	'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36,gzip(gfe)',
	'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.18 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:3.2) Goanna/20170821 PaleMoon/27.4.2',
	'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:42.0) Gecko/20100101 Firefox/42.0',
	'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:45.9) Gecko/20100101 Goanna/3.2 Firefox/45.9 PaleMoon/27.4.2',
	'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0',
	'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0',
	'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0',
	'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534+ (KHTML, like Gecko) BingPreview/1.0b',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.102 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.149 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36; 360Spider',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/7.0.6.1042 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36 OPR/38.0.2220.29',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.1.2909.1213 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36,gzip(gfe)',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.0.12335 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.2991.0 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 YaBrowser/17.7.0.1683 Yowser/2.5 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 YaBrowser/17.7.1.791 Yowser/2.5 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 YaBrowser/17.7.1.804 Yowser/2.5 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36 OPR/46.0.2597.32',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36 Sleipnir/4.5.8',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.90 Safari/537.36 Vivaldi/1.91.867.38',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36 OPR/47.0.2631.71',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36 OPR/47.0.2631.71 (Edition 360-1)',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.4.3112.104 Safari/537.36,gzip(gfe)',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) coc_coc_browser/66.4.102 Chrome/60.4.3112.102 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) coc_coc_browser/66.4.104 Chrome/60.4.3112.104 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:25.0) Gecko/20100101 Firefox/25.0',
	'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20120101 Firefox/29.0',
	'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0',
	'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
	'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
	'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 IceDragon/40.1.1.18 Firefox/40.0.2',
	'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
	'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0',
	'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.9) Gecko/20100101 Goanna/3.2 Firefox/45.9 PaleMoon/27.4.2',
	'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
	'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0',
	'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
	'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0',
	'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
	'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.2.0) Gecko/52.2.0 Firefox/52.2.0; ADSSO',
	'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
	'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
	'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0',
	'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
	'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.2; rv:55.0) Gecko/20100101 Firefox/55.0',
	'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
	'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.12.2987.98 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0',
	'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0',
	'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0',
	'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
	'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.5.3029.81 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0',
	'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36 OPR/44.0.2510.1449',
	'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 OPR/45.0.0.255225845',
	'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36,gzip(gfe)',
	'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0',
	'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
	'Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; Touch; LCJB; rv:11.0) like Gecko',
	'Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; Touch; rv:11.0) like Gecko',
	'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.0.10802 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/7.0.6.1042 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.0.12137 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36 OPR/43.0.2442.1144',
	'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.2988.0 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.90 Safari/537.36 Vivaldi/1.91.867.38',
	'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36 OPR/47.0.2631.80',
	'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) coc_coc_browser/66.4.104 Chrome/60.4.3112.104 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
	'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
	'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0',
	'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; MAFSJS; rv:11.0) like Gecko',
	'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
	'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko/20100101 Firefox/12.0',
	'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; LCJB; rv:11.0) like Gecko',
	'Mozilla/5.0 (Windows Phone 8.1; ARM; Trident/7.0; Touch; rv:11.0; IEMobile/11.0; NOKIA; Lumia 635) like Gecko',
	'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.0.7; Google-SearchByImage) Gecko/2009021910 Firefox/3.0.7',
	'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/3.0.195.27 Safari/532.0',
	'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.3) Gecko/20070309 Firefox/2.0.0.3',
	'Mozilla/5.0 (X11; CrOS x86_64 9460.73.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.134 Safari/537.36',
	'Mozilla/5.0 (X11; CrOS x86_64 9592.85.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.112 Safari/537.36',
	'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
	'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
	'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
	'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0',
	'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.132 Safari/537.36',
	'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36 Google Favicon',
	'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
	'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36',
	'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
	'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36',
	'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
	'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/48.0.2564.82 Chrome/48.0.2564.82 Safari/537.36',
	'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/60.0.3112.113 Chrome/60.0.3112.113 Safari/537.36',
	'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/60.0.3112.78 Chrome/60.0.3112.78 Safari/537.36',
	'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) WordPress.com mShots Safari/537.36',
	'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/44.0 (Chrome)',
	'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/47.0 (Chrome)',
	'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
	'Mozilla/5.0 (X11; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0',
	'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.460.0 Safari/534.3',
	'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.114 Safari/537.36 Puffin/5.2.0IT',
	'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.114 Safari/537.36 Puffin/5.2.2IT',
	'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:41.0) Gecko/20100101 Firefox/41.0',
	'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0',
	'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0',
	'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0',
	'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0',
	'Opera/9.80 (BlackBerry; Opera Mini/8.0.35667/67.445; U; en) Presto/2.12.423 Version/12.16',
	'UCWEB/2.0 (Java; U; MIDP-2.0; Nokia203/20.37) U2/1.0.0 UCBrowser/8.7.0.218 U2/1.0.0 Mobile',
	'UCWEB/2.0 (MIDP-2.0; U; Adr 4.4.2; id; S35G) U2/1.0.0 UCBrowser/10.7.8.806 U2/1.0.0 Mobile',
	'UCWEB/2.0 (MIDP-2.0; U; Adr 5.0.1; en-US; GT-I9500) U2/1.0.0 UCBrowser/10.9.5.983 U2/1.0.0 Mobile',
	'UCWEB/2.0 (MIDP-2.0; U; Adr 5.1.1; en-US; A37f) U2/1.0.0 UCBrowser/10.9.8.1006 U2/1.0.0 Mobile',
	'UCWEB/2.0 (MIDP-2.0; U; Adr 5.1.1; en-US; SM-J200G) U2/1.0.0 UCBrowser/10.6.0.706 U2/1.0.0 Mobile',
	'UCWEB/2.0 (MIDP-2.0; U; Adr 6.0.1; id; ASUS_Z00LDD) U2/1.0.0 UCBrowser/10.9.5.983 U2/1.0.0 Mobile',
	'UCWEB/2.0 (MIDP-2.0; U; Adr 6.0; airg.com; S8_mini) U2/1.0.0 UCBrowser/9.6.0.514 U2/1.0.0 Mobile',
	'UCWEB/2.0 (Windows; U; wds 8.10; en-IN; NOKIA; RM-978_1046) U2/1.0.0 UCBrowser/4.2.1.541 U2/1.0.0 Mobile',


]

ACCEPT_LANGUAGE =[

	"en-gb,en-us;q=0.7,de-ch;q=0.3",
	"en-GB,en-US;q=0.8,en;q=0.6",
	"en-GB,en-US;q=0.8,en;q=0.6",
	"en-US",
	"en-us, en;q=1.0,fr-ca, fr;q=0.5,pt-br, pt;q=0.5,es;q=0.5",
	"en-US,de-DE;q=0.5",
	"en-us,en;q=0.5",
	"en-US,en;q=0.8",
	"en-US,en;q=0.8,en-GB;q=0.6,fr-CA;q=0.4,fr;q=0.2",
	"en-US,en;q=0.8,es-419;q=0.6",
	"en-us,en;q=0.8,es;q=0.5,es-mx;q=0.3",
	"en-US,en;q=0.8,es;q=0.6",
	"en-US,en;q=0.8,pl;q=0.6",
	"en-US,en;q=0.8,pl;q=0.6",
	"en-US,en;q=0.9",
	"en-US,en;q=0.9,fr;q=0.8,de;q=0.7,id;q=0.6",
	"en-US,en;q=0.9,ja;q=0.8,fr;q=0.7,de;q=0.6,es;q=0.5,it;q=0.4,nl;q=0.3,sv;q=0.2,nb;q=0.1",

]

ACCEPT = [
		["text/html","application/xhtml+xml","application/xml;q=0.9"],
		["application/xml","application/xhtml+xml","text/html;q=0.9"," text/plain;q=0.8","image/png"],
		["text/html","application/xhtml+xml","application/xml;q=0.9"],
		["image/jpeg","application/x-ms-application","image/gif","application/xaml+xml","image/pjpeg","application/x-ms-xbap","application/x-shockwave-flash","application/msword"],
		["text/html","application/xml;q=0.9","application/xhtml+xml","image/png","image/webp","image/jpeg","image/gif","image/x-xbitmap"]
]

ACCEPT_POSTFIX = ["*/*;q=0.8", "*/*;q=0.5", "*/*;q=0.8", "*/*", "*/*;q=0.1"]

ENCODINGS = [['gzip'], ['gzip', 'deflate'], ['gzip', 'deflate', 'sdch']]


def getUserAgent():
	'''
	Generate a randomized user agent by permuting a large set of possible values.
	The returned user agent should look like a valid, in-use brower, with a specified preferred language of english.

	Return value is a list of tuples, where each tuple is one of the user-agent headers.

	Currently can provide approximately 147 * 17 * 5 * 5 * 2 * 3 * 2 values, or ~749K possible
	unique user-agents.
	'''
	coding = random.choice(ENCODINGS)
	random.shuffle(coding)
	coding = ",".join(coding)

	accept = random.choice(ACCEPT)
	random.shuffle(accept)
	accept.append(random.choice(ACCEPT_POSTFIX))
	accept = random.choice((", ", ",")).join(accept)

	user_agent = [
				('User-Agent'		,	random.choice(USER_AGENTS)),
				('Accept-Language'	,	random.choice(ACCEPT_LANGUAGE)),
				('Accept'			,	accept),
				('Accept-Encoding'	,	coding)
				]
	return user_agent




# This file based heavily on the UA List, Copyright (c) 2014, Harald Hope
# This list was released under the BSD 2 clause.

# Home page: techpatterns.com/forums/about304.html

# Special thanks to the following:
# User-Agent Switcher: www.chrispederick.com/work/user-agent-switcher
# Firefox history: www.zytrax.com/tech/web/firefox-history.html
# Mobile data: wikipedia.org/wiki/List_of_user_agents_for_mobile_phones
# Mobile data: www.zytrax.com/tech/web/mobile_ids.html
# Current User-Agents: http://myip.ms/browse/comp_browsers
# User-agent data: www.zytrax.com/tech/web/browser_ids.htm
# User-agent strings: www.useragentstring.com
# User-agent strings: www.webapps-online.com/online-tools/user-agent-strings/dv/

# License: BSD 2 Clause
# All rights reserved. Redistribution and use in source and binary forms,
# with or without modification, are permitted provided that the following
# conditions are met:
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice, this
# list of conditions and the following disclaimer in the documentation and/or other
# materials provided with the distribution.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 'AS IS'
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.




if __name__ == "__main__":
	import logSetup
	import sys
	logSetup.initLogging()
	print("Oh HAI")
	wg = WebGetRobust()

	if len(sys.argv) == 3:
		getUrl = sys.argv[1]
		fName  = sys.argv[2]
		print(getUrl, fName)

		content = wg.getpage(getUrl)

		try:
			out = content.encode("utf-8")
		except:
			out = content

		with open(fName, 'wb') as fp:
			fp.write(out)


	print("Working")
	ret = wg.getHeadTitlePhantomJS("http://www.google.com/", referrer="http://www.google.com/")
	print("Ret:")
	print(ret)
	content, handle = wg.getpage("http://japtem.com/wp-content/uploads/2014/07/Arifureta.png", returnMultiple = True)
	print((handle.headers.get('Content-Encoding')))
	print(len(content))
	content, handle = wg.getpage("http://japtem.com/wp-content/uploads/2014/03/knm.png", returnMultiple = True)
	print((handle.headers.get('Content-Encoding')))
	content, handle = wg.getpage("https://www.google.com/images/srpr/logo11w.png", returnMultiple = True)
	print((handle.headers.get('Content-Encoding')))
	content, handle = wg.getpage("http://www.doujin-moe.us/ajax/newest.php", returnMultiple = True)
	print((handle.headers.get('Content-Encoding')))

	print("SoupGet")
	content_1 = wg.getpage("http://www.lighttpd.net", soup = True)

	content_2 = wg.getSoup("http://www.lighttpd.net")
	assert(content_1 == content_2)

	gTest = wg.getpage('https://drive.google.com/folderview?id=0B2lnOX3NF2LOeW55WlpYQWIxYnM')
	print(type(gTest))

	gTest = wg.getpage('https://www.google.com/search?q=Gödel')
	gTest = wg.getpage('https://www.google.com/search?q=禁断の愛')
	gTest = wg.getpage('http://www.fanfiction.net/s/6711282/1/Jag-%C3%A4lskar-dig')
	print(type(gTest))



# if __name__ == "__main__":
# 	print("User agent", getUserAgent())
