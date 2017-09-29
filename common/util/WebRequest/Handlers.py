#!/usr/bin/python3
import sys
import codecs

import http.client
import email.parser

import urllib.request
import urllib.parse
import urllib.error

import os.path

import time
import http.cookiejar

import traceback

import logging
import zlib
import bs4
import re
import string
import gzip
import io
import socket
import json
import base64

import random

class HeadRequest(urllib.request.Request):
	def get_method(self):
		# Apparently HEAD is now being blocked. Because douche.
		return "GET"
		# return "HEAD"

class HTTPRedirectBlockerErrorHandler(urllib.request.HTTPErrorProcessor):    # pragma: no cover

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
		if new is None:    # pragma: no cover
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
