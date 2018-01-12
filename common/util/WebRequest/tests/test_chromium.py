import unittest
import socket
import json
import base64
import zlib
import gzip
import bs4
import ChromeController
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
			self.wfile.write(b"<html><body>Root OK?</body></html>")

		if self.path == "/with_title_1":
			self.send_response(200)
			self.send_header('Content-type', "text/html")
			self.end_headers()
			self.wfile.write(b"<html><html><title>Page Title 1</title></html><body>Root OK?</body></html>")

		elif self.path == "/raw-txt":
			self.send_response(200)
			self.send_header('Content-type', "text/plain")
			self.end_headers()
			self.wfile.write(b"Root OK?")

		elif self.path == "/binary_ctnt":
			self.send_response(200)
			self.send_header('Content-type', "image/jpeg")
			self.end_headers()
			self.wfile.write(b"Binary!\x00\x01\x02\x03")

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


class TestChromium(unittest.TestCase):
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

		# Hacky force-close of the chromium interface
		# self.wg.close_chromium()
		del self.wg

	def test_fetch_1(self):
		page = self.wg.getpage("http://localhost:{}".format(self.mock_server_port))
		self.assertEqual(page, '<html><body>Root OK?</body></html>')

	def test_fetch_chromium_1(self):
		page, fname, mtype = self.wg.getItemChromium("http://localhost:{}".format(self.mock_server_port))

		self.assertEqual(fname, '')
		self.assertEqual(mtype, 'text/html')
		self.assertEqual(page, '<html><body>Root OK?</body></html>')

	def test_fetch_chromium_2(self):
		page, fname, mtype = self.wg.getItemChromium("http://localhost:{}/raw-txt".format(self.mock_server_port))
		self.assertEqual(fname, 'raw-txt')
		self.assertEqual(mtype, 'text/html')  # I'm not properly retrieving the mimetype from chromium
		self.assertEqual(page, 'Root OK?')

	def test_fetch_chromium_3(self):
		page, fname, mtype = self.wg.getItemChromium("http://localhost:{}/binary_ctnt".format(self.mock_server_port))
		self.assertEqual(fname, 'binary_ctnt')
		self.assertEqual(mtype, 'application/x-binary')
		self.assertEqual(page, b"Binary!\x00\x01\x02\x03")

	def test_head_chromium_1(self):
		url_1 = "http://localhost:{}/raw-txt".format(self.mock_server_port)
		purl_1 = self.wg.getHeadChromium(url_1)
		self.assertEqual(purl_1, url_1)

	def test_head_chromium_2(self):
		url_2 = "http://localhost:{}/redirect/to-1".format(self.mock_server_port)
		purl_2 = self.wg.getHeadChromium("http://localhost:{}/redirect/from-1".format(self.mock_server_port))
		self.assertEqual(purl_2, url_2)

	def test_head_chromium_3(self):
		url_3 = "http://localhost:{}/redirect/bad-1".format(self.mock_server_port)
		purl_3 = self.wg.getHeadChromium("http://localhost:{}/redirect/bad-1".format(self.mock_server_port))
		self.assertEqual(purl_3, url_3)

	def test_head_chromium_4(self):
		# Chromium changes infinite redirects into timeouts.
		with self.assertRaises(ChromeController.ChromeNavigateTimedOut):
			self.wg.getHeadChromium("http://localhost:{}/redirect/bad-2".format(self.mock_server_port))

	def test_head_chromium_5(self):
		# Chromium changes infinite redirects into timeouts.
		with self.assertRaises(ChromeController.ChromeNavigateTimedOut):
			self.wg.getHeadChromium("http://localhost:{}/redirect/bad-3".format(self.mock_server_port))

	def test_head_title_chromium_1(self):
		pg_url = "http://localhost:{}/with_title_1".format(self.mock_server_port)
		retreived = self.wg.getHeadTitleChromium(pg_url)

		expect = {
						'url': pg_url,
						'title': 'Page Title 1',
		}
		self.assertEqual(retreived, expect)

	def test_head_title_chromium_2(self):
		pg_url = "http://localhost:{}/".format(self.mock_server_port)
		retreived = self.wg.getHeadTitleChromium(pg_url)

		expect = {
						# If no title is specified, chromium returns the server URL
						'url': pg_url,
						'title': 'localhost:{}'.format(self.mock_server_port),
		}
		self.assertEqual(retreived, expect)

	def test_head_title_chromium_3(self):
		pg_url = "http://localhost:{}/binary_ctnt".format(self.mock_server_port)
		retreived = self.wg.getHeadTitleChromium(pg_url)

		expect = {
						# If no title is specified, chromium returns the server URL
						'url': pg_url,
						'title': 'localhost:{}/binary_ctnt'.format(self.mock_server_port),
		}
		self.assertEqual(retreived, expect)
