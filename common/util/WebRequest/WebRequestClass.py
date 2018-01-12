#!/usr/bin/python3
import urllib.request
import urllib.parse
import urllib.error


import os.path

import time
import http.cookiejar

import traceback

import logging
import zlib
import codecs
import re
import sys
import gzip
import io
import socket
import json

from threading import Lock

import bs4
try:
	import socks
	from sockshandler import SocksiPyHandler
	HAVE_SOCKS = True
except ImportError:
	HAVE_SOCKS = False

from . import HeaderParseMonkeyPatch

from . import ChromiumMixin
from . import PhantomJSMixin
from . import Handlers
from . import iri2uri
from . import Constants
from . import Exceptions

#pylint: disable-msg=E1101, C0325, R0201, W0702, W0703

COOKIEWRITELOCK = Lock()

GLOBAL_COOKIE_FILE = None

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
			raise Exceptions.ContentTypeError("Unknown encoding!")

	elif len(json_bytes) > 2:
		b1, b2 = json_bytes[0], json_bytes[1]
		if   b1 == 0 and b2 == 0:
			return "UTF-32BE"
		elif b1 == 0 and b2 != 0:
			return "UTF-16BE"
		elif b1 != 0 and b2 == 0:
			raise Exceptions.ContentTypeError("Json string too short to definitively infer encoding.")
		elif b1 != 0 and b2 != 0:
			return "UTF-8"
		else:
			raise Exceptions.ContentTypeError("Unknown encoding!")

	raise Exceptions.ContentTypeError("Input string too short to guess encoding!")


# A urllib2 wrapper that provides error handling and logging, as well as cookie management. It's a bit crude, but it works.
# Also supports transport compresion.
# OOOOLLLLLLDDDDD, has lots of creaky internals. Needs some cleanup desperately, but lots of crap depends on almost everything.
# Arrrgh.

class WebGetRobust(PhantomJSMixin.WebGetPjsMixin, ChromiumMixin.WebGetCrMixin):

	COOKIEFILE = 'cookies.lwp'				# the path and filename to save your cookies in
	cj = None
	cookielib = None
	opener = None

	errorOutCount = 2
	# retryDelay = 0.1
	retryDelay = 0.01

	data = None

	# creds is a list of 3-tuples that gets inserted into the password manager.
	# it is structured [(top_level_url1, username1, password1), (top_level_url2, username2, password2)]
	def __init__(self, creds=None, logPath="Main.WebRequest", cookie_lock=None,  cloudflare=True, use_socks=False, alt_cookiejar=None):
		super().__init__()

		self.rules = {}
		self.rules['cloudflare'] = cloudflare
		if cookie_lock:
			self.cookie_lock = cookie_lock
		else:
			self.cookie_lock = COOKIEWRITELOCK

		self.use_socks = use_socks
		# Override the global default socket timeout, so hung connections will actually time out properly.
		socket.setdefaulttimeout(5)

		self.log = logging.getLogger(logPath)
		# print("Webget init! Logpath = ", logPath)
		if creds:
			print("Have creds for a domain")

		# Due to general internet people douchebaggyness, I've basically said to hell with it and decided to spoof a whole assortment of browsers
		# It should keep people from blocking this scraper *too* easily
		self.browserHeaders = Constants.getUserAgent()

		self.data = urllib.parse.urlencode(self.browserHeaders)

		if creds:
			print("Have credentials, installing password manager into urllib handler.")
			passManager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
			for url, username, password in creds:
				passManager.add_password(None, url, username, password)
			self.credHandler = Handlers.PreemptiveBasicAuthHandler(passManager)
		else:
			self.credHandler = None

		self.alt_cookiejar = alt_cookiejar
		self.__loadCookies()
	def chunkReport(self, bytesSoFar, totalSize):
		if totalSize:
			percent = float(bytesSoFar) / totalSize
			percent = round(percent * 100, 2)
			self.log.info("Downloaded %d of %d bytes (%0.2f%%)" % (bytesSoFar, totalSize, percent))
		else:
			self.log.info("Downloaded %d bytes" % (bytesSoFar))

	def __chunkRead(self, response, chunkSize=2 ** 18, reportHook=None):
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
			raise Exceptions.ArgumentError("getSoup cannot be called with 'returnMultiple' being true")

		if 'soup' in kwargs and kwargs['soup']:
			raise Exceptions.ArgumentError("getSoup contradicts the 'soup' directive!")

		page = self.getpage(*args, **kwargs)
		if isinstance(page, bytes):
			raise Exceptions.ContentTypeError("Received content not decoded! Cannot parse!")

		soup = as_soup(page)
		return soup

	def getJson(self, *args, **kwargs):
		if 'returnMultiple' in kwargs and kwargs['returnMultiple']:
			raise Exceptions.ArgumentError("getSoup cannot be called with 'returnMultiple' being true")

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
					self.log.error("JSON Parsing issue retrieving content from page!")
					for line in traceback.format_exc().split("\n"):
						self.log.error("%s", line.rstrip())
					self.log.error("Retrying!")

					# Scramble our current UA
					self.browserHeaders = Constants.getUserAgent()
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

	def getFileAndName(self, *args, **kwargs):
		if 'returnMultiple' in kwargs:
			raise Exceptions.ArgumentError("getFileAndName cannot be called with 'returnMultiple'")

		if 'soup' in kwargs and kwargs['soup']:
			raise Exceptions.ArgumentError("getFileAndName contradicts the 'soup' directive!")

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

	def getFileNameMime(self, *args, **kwargs):
		if 'returnMultiple' in kwargs:
			raise Exceptions.ArgumentError("getFileAndName cannot be called with 'returnMultiple'")

		if 'soup' in kwargs and kwargs['soup']:
			raise Exceptions.ArgumentError("getFileAndName contradicts the 'soup' directive!")

		kwargs["returnMultiple"] = True

		pgctnt, pghandle = self.getpage(*args, **kwargs)

		info = pghandle.info()
		if not 'Content-Disposition' in info:
			hName = ''
		elif not 'filename=' in info['Content-Disposition']:
			hName = ''
		else:
			hName = info['Content-Disposition'].split('filename=')[1]

		mime = info.get_content_type()

		return pgctnt, hName, mime

	def __getpage(self, requestedUrl, **kwargs):
		self.log.info("Fetching content at URL: %s", requestedUrl)

		# strip trailing and leading spaces.
		requestedUrl = requestedUrl.strip()

		# If we have 'soup' as a param, just pop it, and call `getSoup()`.
		if 'soup' in kwargs and kwargs['soup']:
			self.log.warning("'soup' kwarg is depreciated. Please use the `getSoup()` call instead.")
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
			addlHeaders['Referer'] = iri2uri.iri2uri(addlHeaders['Referer'])


		retryCount = 0
		while 1:

			pgctnt = None
			pghandle = None

			pgreq = self.__buildRequest(requestedUrl, postData, addlHeaders, binaryForm)

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

			except Exceptions.GarbageSiteWrapper as e:
				print("garbage site:")
				raise e

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
						self.log.warning("Cloudflare failure! Doing automatic step-through.")
						raise Exceptions.CloudFlareWrapper("WAF Shit")

			except UnicodeEncodeError:
				self.log.critical("Unrecoverable Unicode issue retrieving page - %s", requestedUrl)
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
				self.log.warning(str(lastErr))
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
				pgctnt = self.__retreiveContent(pgreq, pghandle, callBack)


				# if __retreiveContent did not return false, it managed to fetch valid results, so break
				if pgctnt != False:
					break

		if errored and pghandle != None:
			print(("Later attempt succeeded %s" % pgreq.get_full_url()))
		elif (errored or not pgctnt) and pghandle is None:

			if lastErr and nativeError:
				raise lastErr
			raise Exceptions.FetchFailureError("Failed to retreive page '%s'!" % (requestedUrl, ))

		if returnMultiple:

			return pgctnt, pghandle
		else:
			return pgctnt

	def getpage(self, requestedUrl, *args, **kwargs):
		try:
			return self.__getpage(requestedUrl, *args, **kwargs)

		except Exceptions.CloudFlareWrapper:
			print("Failure?")
			if self.rules['cloudflare']:
				if not self.stepThroughCloudFlare(requestedUrl, titleNotContains='Just a moment...'):
					raise Exceptions.FetchFailureError("Could not step through cloudflare!")
				# Cloudflare cookie set, retrieve again
				return self.__getpage(requestedUrl, *args, **kwargs)

			else:
				raise

		except Exceptions.SucuriWrapper:
			if self.rules['cloudflare']:
				if not self.stepThroughCloudFlare(requestedUrl, titleNotContains="You are being redirected..."):
					raise Exceptions.FetchFailureError("Could not step through Sucuri WAF bullshit!")
				return self.__getpage(requestedUrl, *args, **kwargs)
			else:
				print("not handled?")
				raise

	def getItem(self, itemUrl):

		content, handle = self.getpage(itemUrl, returnMultiple=True)

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

	def getHead(self, url, addlHeaders=None):
		for x in range(9999):
			try:
				self.log.info("Doing HTTP HEAD request for '%s'", url)
				pgreq = self.__buildRequest(url, None, addlHeaders, None, req_class=Handlers.HeadRequest)
				pghandle = self.opener.open(pgreq, timeout=30)
				returl = pghandle.geturl()
				if returl != url:
					self.log.info("HEAD request returned a different URL '%s'", returl)

				return returl
			except socket.timeout as e:
				self.log.info("Timeout, retrying....")
				if x >= 3:
					self.log.error("Failure fetching: %s", url)
					raise Exceptions.FetchFailureError("Timout when fetching %s. Error: %s" % (url, e))
			except urllib.error.URLError as e:
				# Continue even in the face of cloudflare crapping it's pants
				if e.code == 500 and e.geturl():
					return e.geturl()
				self.log.info("URLError, retrying....")
				if x >= 3:
					self.log.error("Failure fetching: %s", url)
					raise Exceptions.FetchFailureError("URLError when fetching %s. Error: %s" % (url, e))

	######################################################################################################################################################
	######################################################################################################################################################

	def __decodeHtml(self, pageContent, cType):

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

	def __buildRequest(self, pgreq, postData, addlHeaders, binaryForm, req_class = None):
		if req_class is None:
			req_class = urllib.request.Request

		pgreq = iri2uri.iri2uri(pgreq)

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
					raise Exceptions.ArgumentError("You cannot make a binary form post and a plain post request at the same time!")

				params['data']            = binaryForm.make_result()
				headers['Content-type']   =  binaryForm.get_content_type()
				headers['Content-length'] =  len(params['data'])

			return req_class(pgreq, headers=headers, **params)

		except:
			self.log.critical("Invalid header or url")
			raise

	def __decompressContent(self, coding, pgctnt):
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
			raise Exceptions.ContentTypeError("Wait, someone other then google actually supports SDCH compression?")

		else:
			compType = "none"

		return compType, pgctnt

	def __decodeTextContent(self, pgctnt, cType):

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

					pgctnt = self.__decodeHtml(pgctnt, cType)

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

	def __retreiveContent(self, pgreq, pghandle, callBack):
		try:
			# If we have a progress callback, call it for chunked read.
			# Otherwise, just read in the entire content.
			if callBack:
				pgctnt = self.__chunkRead(pghandle, 2 ** 17, reportHook=callBack)
			else:
				pgctnt = pghandle.read()


			if pgctnt is None:
				return False

			self.log.info("URL fully retrieved.")

			preDecompSize = len(pgctnt)/1000.0

			encoded = pghandle.headers.get('Content-Encoding')
			compType, pgctnt = self.__decompressContent(encoded, pgctnt)


			decompSize = len(pgctnt)/1000.0
			# self.log.info("Page content type = %s", type(pgctnt))
			cType = pghandle.headers.get("Content-Type")
			if compType == 'none':
				self.log.info("Compression type = %s. Content Size = %0.3fK. File type: %s.", compType, decompSize, cType)
			else:
				self.log.info("Compression type = %s. Content Size compressed = %0.3fK. Decompressed = %0.3fK. File type: %s.", compType, preDecompSize, decompSize, cType)

			if b"sucuri_cloudproxy_js=" in pgctnt:
				raise Exceptions.SucuriWrapper("WAF Shit")
			pgctnt = self.__decodeTextContent(pgctnt, cType)

			return pgctnt


		except Exceptions.SucuriWrapper:
			print("garbage site:")
			raise


		except:

			self.log.error(sys.exc_info())
			traceback.print_exc()
			self.log.error("Error Retrieving Page! - Transfer failed. Waiting %s seconds before retrying", self.retryDelay)

			try:
				self.log.critical("Critical Failure to retrieve page! %s at %s", pgreq.get_full_url(), time.ctime(time.time()))
				self.log.critical("Exiting")
			except:
				self.log.critical("And the URL could not be printed due to an encoding error")
			self.log.error(pghandle)
			time.sleep(self.retryDelay)

		return False


		# HUGE GOD-FUNCTION.
		# OH GOD FIXME.

		# postData expects a dict
		# addlHeaders also expects a dict

	######################################################################################################################################################
	######################################################################################################################################################

	def __loadCookies(self):

		if self.alt_cookiejar is not None:
			self.alt_cookiejar.init_agent(new_headers=self.browserHeaders)
			self.cj = self.alt_cookiejar
		else:
			self.cj = http.cookiejar.LWPCookieJar()		# This is a subclass of FileCookieJar
												# that has useful load and save methods
		if self.cj is not None:
			if os.path.isfile(self.COOKIEFILE):
				try:
					self.__updateCookiesFromFile()
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
				args = (cookieHandler, Handlers.HTTPRedirectHandler)
				if self.credHandler:
					print("Have cred handler. Building opener using it")
					args += (self.credHandler, )
				if self.use_socks:
					print("Using Socks handler")
					if not HAVE_SOCKS:
						raise RuntimeError("SOCKS Use specified, and no socks installed!")
					args = (SocksiPyHandler(socks.SOCKS5, "127.0.0.1", 9050), ) + args

				self.opener = urllib.request.build_opener(*args)
				#self.opener.addheaders = [('User-Agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')]
				self.opener.addheaders = self.browserHeaders
				#urllib2.install_opener(self.opener)

		for cookie in self.cj:
			self.log.debug(cookie)
			#print cookie

	def _syncCookiesFromFile(self):
		# self.log.info("Synchronizing cookies with cookieFile.")
		if os.path.isfile(self.COOKIEFILE):
			self.cj.save("cookietemp.lwp")
			self.cj.load(self.COOKIEFILE)
			self.cj.load("cookietemp.lwp")
		# First, load any changed cookies so we don't overwrite them
		# However, we want to persist any cookies that we have that are more recent then the saved cookies, so we temporarily save
		# the cookies in memory to a temp-file, then load the cookiefile, and finally overwrite the loaded cookies with the ones from the
		# temp file

	def __updateCookiesFromFile(self):
		if os.path.exists(self.COOKIEFILE):
			# self.log.info("Synchronizing cookies with cookieFile.")
			self.cj.load(self.COOKIEFILE)
		# Update cookies from cookiefile

	def addCookie(self, inCookie):
		self.log.info("Updating cookie!")
		self.cj.set_cookie(inCookie)

	def saveCookies(self, halting=False):

		locked = self.cookie_lock.acquire(timeout=5)
		if not locked:
			self.log.error("Failed to acquire cookie-lock!")
			return

		# print("Have %d cookies before saving cookiejar" % len(self.cj))
		try:
			# self.log.info("Trying to save cookies!")
			if self.cj is not None:							# If cookies were used

				self._syncCookiesFromFile()

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
			self._syncCookiesFromFile()
		# print "Have %d cookies after reloading cookiejar" % len(self.cj)

	def getCookies(self):

		locked = self.cookie_lock.acquire(timeout=5)
		if not locked:
			raise RuntimeError("Could not acquire lock on cookiejar")

		try:
			# self.log.info("Trying to save cookies!")
			if self.cj is not None:							# If cookies were used
				self._syncCookiesFromFile()
		finally:
			self.cookie_lock.release()

		return self.cj

	######################################################################################################################################################
	######################################################################################################################################################

	def __del__(self):
		# print "WGH Destructor called!"
		# print("WebRequest __del__")
		self.saveCookies(halting=True)

		sup = super()
		if hasattr(sup, '__del__'):
			sup.__del__()




	def stepThroughCloudFlare(self, *args, **kwargs):
		# Shim to the underlying web browser of choice

		return self.stepThroughCloudFlare_pjs(*args, **kwargs)


