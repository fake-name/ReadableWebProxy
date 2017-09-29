import unittest
import socket
import json
import base64
import zlib
import gzip
import bs4
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread

import util.WebRequest as WebRequest


class MockServerRequestHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		# Process an HTTP GET request and return a response with an HTTP 200 status.
		print("Path: ", self.path)

		if self.path == "/":
			self.send_response(200)
			self.send_header('Content-type', "text/html")
			self.end_headers()
			self.wfile.write(b"Root OK?")

		elif self.path == "/raw-txt":
			self.send_response(200)
			self.send_header('Content-type', "text/plain")
			self.end_headers()
			self.wfile.write(b"Root OK?")

		elif self.path == "/redirect/bad-1":
			self.send_response(302)
			self.end_headers()

		elif self.path == "/redirect/bad-2":
			self.send_response(302)
			self.send_header('location', "bad-2")
			self.end_headers()

		elif self.path == "/redirect/bad-3":
			self.send_response(302)
			self.send_header('location', "gopher://www.google.com")
			self.end_headers()

		elif self.path == "/redirect/from-1":
			self.send_response(302)
			self.send_header('location', "to-1")
			self.end_headers()

		if self.path == "/redirect/to-1":
			self.send_response(200)
			self.end_headers()
			self.wfile.write(b"Redirect-To-1")

		elif self.path == "/redirect/from-2":
			self.send_response(302)
			self.send_header('uri', "to-2")
			self.end_headers()

		if self.path == "/redirect/to-2":
			self.send_response(200)
			self.end_headers()
			self.wfile.write(b"Redirect-To-2")

		elif self.path == "/redirect/from-3":
			self.send_response(302)
			newurl = "http://{}:{}".format(self.server.server_address[0], self.server.server_address[1])
			self.send_header('uri', newurl)
			self.end_headers()


def get_free_port():
	s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
	s.bind(('localhost', 0))
	address, port = s.getsockname()
	s.close()
	return port


class TestPhantomJS(unittest.TestCase):
	def setUp(self):

		# Configure mock server.
		self.mock_server_port = get_free_port()
		self.mock_server = HTTPServer(('localhost', self.mock_server_port), MockServerRequestHandler)

		# Start running mock server in a separate thread.
		# Daemon threads automatically shut down when the main process exits.
		self.mock_server_thread = Thread(target=self.mock_server.serve_forever)
		self.mock_server_thread.setDaemon(True)
		self.mock_server_thread.start()
		self.wg = WebRequest.WebGetRobust()

	def tearDown(self):
		self.mock_server.shutdown()

	def test_fetch_1(self):
		page = self.wg.getpage("http://localhost:{}".format(self.mock_server_port))
		self.assertEqual(page, 'Root OK?')

	def test_fetch_pjs(self):
		page_1, fname_1, mtype_1 = self.wg.getItemPhantomJS("http://localhost:{}".format(self.mock_server_port))
		# I think all this garbage is phantomjs/selenium deciding they know what I want the content to look like for me.
		# Note that the content isn't specified to be HTML ANYWHERE.
		self.assertEqual(page_1, '<html><head></head><body>Root OK?</body></html>')

		# Because PJS is retarded, it ALWAYS wraps content in html shit unless you specify the content is "text/html". If you do that, it then proceds to only
		# add /some/ of the html tag garbage
		page_2, fname_2, mtype_2 = self.wg.getItemPhantomJS("http://localhost:{}/raw-txt".format(self.mock_server_port))
		# I think all this garbage is phantomjs/selenium deciding they know what I want the content to look like for me.
		# Note that the content isn't specified to be HTML ANYWHERE.
		self.assertEqual(
						page_2,
						'<html><head></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">Root OK?</pre></body></html>'
		)

	def test_head_pjs_1(self):
		url_1 = "http://localhost:{}/raw-txt".format(self.mock_server_port)
		purl_1 = self.wg.getHeadPhantomJS(url_1)
		self.assertEqual(purl_1, url_1)

		url_2 = "http://localhost:{}/redirect/to-1".format(self.mock_server_port)
		purl_2 = self.wg.getHeadPhantomJS("http://localhost:{}/redirect/from-1".format(self.mock_server_port))
		self.assertEqual(purl_2, url_2)

	# We expect to get the same value as passed, since pjs will not resolve out
	# the bad redirects.
	# Note we have to restart phantomjs for these tests, because otherwise it remembers state (this is why they're separate tests).
	def test_head_pjs_2(self):
		url_3 = "http://localhost:{}/redirect/bad-1".format(self.mock_server_port)
		purl_3 = self.wg.getHeadPhantomJS("http://localhost:{}/redirect/bad-1".format(self.mock_server_port))
		self.assertEqual(purl_3, url_3)

	def test_head_pjs_3(self):
		# Somehow, this turns into 'about:blank'. NFI how
		url_4 = "about:blank"
		purl_4 = self.wg.getHeadPhantomJS("http://localhost:{}/redirect/bad-2".format(self.mock_server_port))
		self.assertEqual(purl_4, url_4)

	def test_head_pjs_4(self):
		# Somehow, this turns into 'about:blank'. NFI how
		url_5 = "about:blank"
		purl_5 = self.wg.getHeadPhantomJS("http://localhost:{}/redirect/bad-3".format(self.mock_server_port))
		self.assertEqual(purl_5, url_5)
