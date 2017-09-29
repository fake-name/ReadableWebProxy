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


class TestPlainCreation(unittest.TestCase):
	def test_plain_instantiation_1(self):
		wg = WebRequest.WebGetRobust()
		self.assertTrue(wg is not None)

	def test_plain_instantiation_2(self):
		wg = WebRequest.WebGetRobust(cloudflare=True)
		self.assertTrue(wg is not None)

	def test_plain_instantiation_3(self):
		wg = WebRequest.WebGetRobust(use_socks=True)
		self.assertTrue(wg is not None)


class MockServerRequestHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		# Process an HTTP GET request and return a response with an HTTP 200 status.
		print("Path: ", self.path)

		if self.path == "/":
			self.send_response(200)
			self.end_headers()
			self.wfile.write(b"Root OK?")

		elif self.path == "/html-decode":
			self.send_response(200)
			self.send_header('Content-type', "text/html")
			self.end_headers()
			self.wfile.write(b"Root OK?")

		elif self.path == "/html/real":
			self.send_response(200)
			self.send_header('Content-type', "text/html")
			self.end_headers()
			self.wfile.write(b"<html><body>Root OK?</body></html>")

		elif self.path == "/compressed/deflate":
			self.send_response(200)
			self.send_header('Content-Encoding', 'deflate')
			self.send_header('Content-type', "text/html")
			self.end_headers()

			inb = b"Root OK?"
			cobj = zlib.compressobj(wbits=-zlib.MAX_WBITS)
			t1 = cobj.compress(inb) + cobj.flush()
			self.wfile.write(t1)

		elif self.path == "/compressed/gzip":
			self.send_response(200)
			self.send_header('Content-Encoding', 'gzip')
			self.send_header('Content-type', "text/html")
			self.end_headers()
			self.wfile.write(gzip.compress(b"Root OK?"))

		elif self.path == "/json/invalid":
			self.send_response(200)
			self.send_header('Content-type', "text/html")
			self.end_headers()
			self.wfile.write(b"LOLWAT")

		elif self.path == "/json/valid":
			self.send_response(200)
			self.send_header('Content-type', "text/html")
			self.end_headers()
			self.wfile.write(b'{"oh" : "hai"}')

		elif self.path == "/json/no-coding":
			self.send_response(200)
			self.end_headers()
			self.wfile.write(b'{"oh" : "hai"}')

		elif self.path == "/filename/path-only.txt":
			self.send_response(200)
			self.end_headers()
			self.wfile.write(b"LOLWAT?")
		elif self.path == "/filename/content-disposition":
			self.send_response(200)
			self.send_header('Content-Disposition', "filename=lolercoaster.txt")
			self.end_headers()
			self.wfile.write(b"LOLWAT?")

		elif self.path == "/filename_mime/path-only.txt":
			self.send_response(200)
			self.end_headers()
			self.wfile.write(b"LOLWAT?")

		elif self.path == "/filename_mime/content-disposition":
			self.send_response(200)
			self.send_header('Content-Disposition', "filename=lolercoaster.txt")
			self.end_headers()
			self.wfile.write(b"LOLWAT?")

		elif self.path == "/filename_mime/content-disposition-html-suffix":
			self.send_response(200)
			self.send_header('Content-Disposition', "filename=lolercoaster.html")
			self.end_headers()
			self.wfile.write(b"LOLWAT?")

		elif self.path == "/filename_mime/explicit-html-mime":
			self.send_response(200)
			self.send_header('Content-Disposition', "filename=lolercoaster.html")
			self.send_header('Content-type', "text/html")
			self.end_headers()
			self.wfile.write(b"LOLWAT?")

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

		elif self.path == "/password/expect":

			self.send_response(200)
			self.end_headers()

			val = self.headers['Authorization']
			passval = val.split(" ")[-1]
			passstr = base64.b64decode(passval)

			if passstr == b'lol:wat':
				self.wfile.write(b"Password Ok?")
			else:
				self.wfile.write(b"Password Bad!")


def get_free_port():
	s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
	s.bind(('localhost', 0))
	address, port = s.getsockname()
	s.close()
	return port


class TestSimpleFetch(unittest.TestCase):
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
		self.assertEqual(page, b'Root OK?')

	def test_fetch_decode_1(self):
		# text/html content should be decoded automatically.
		page = self.wg.getpage("http://localhost:{}/html-decode".format(self.mock_server_port))
		self.assertEqual(page, 'Root OK?')

	def test_fetch_soup(self):
		# text/html content should be decoded automatically.
		page = self.wg.getSoup("http://localhost:{}/html/real".format(self.mock_server_port))
		self.assertEqual(page, bs4.BeautifulSoup('<html><body>Root OK?</body></html>', 'lxml'))

		page = self.wg.getSoup("http://localhost:{}/html-decode".format(self.mock_server_port))
		self.assertEqual(page, bs4.BeautifulSoup('<html><body><p>Root OK?</p></body></html>', 'lxml'))

		# getSoup fails to fetch content that's not of content-type text/html
		with self.assertRaises(WebRequest.ContentTypeError):
			page = self.wg.getSoup("http://localhost:{}/".format(self.mock_server_port))

	def test_fetch_decode_json(self):
		# text/html content should be decoded automatically.
		page = self.wg.getJson("http://localhost:{}/json/valid".format(self.mock_server_port))
		self.assertEqual(page, {'oh': 'hai'})

		page = self.wg.getJson("http://localhost:{}/json/no-coding".format(self.mock_server_port))
		self.assertEqual(page, {'oh': 'hai'})

		with self.assertRaises(json.decoder.JSONDecodeError):
			page = self.wg.getJson("http://localhost:{}/json/invalid".format(self.mock_server_port))

	def test_fetch_compressed(self):

		page = self.wg.getpage("http://localhost:{}/compressed/gzip".format(self.mock_server_port))
		self.assertEqual(page, 'Root OK?')

		page = self.wg.getpage("http://localhost:{}/compressed/deflate".format(self.mock_server_port))
		self.assertEqual(page, 'Root OK?')

	def test_file_and_name(self):
		page, fn = self.wg.getFileAndName("http://localhost:{}/filename/path-only.txt".format(self.mock_server_port))
		self.assertEqual(page, b'LOLWAT?')
		self.assertEqual(fn, '')

		page, fn = self.wg.getFileAndName("http://localhost:{}/filename/content-disposition".format(self.mock_server_port))
		self.assertEqual(page, b'LOLWAT?')
		self.assertEqual(fn, 'lolercoaster.txt')

	def test_file_name_mime(self):
		page, fn, mimet = self.wg.getFileNameMime(
						"http://localhost:{}/filename_mime/path-only.txt".format(self.mock_server_port))
		self.assertEqual(page, b'LOLWAT?')
		self.assertEqual(fn, '')
		self.assertEqual(mimet, 'text/plain')

		page, fn, mimet = self.wg.getFileNameMime(
						"http://localhost:{}/filename_mime/content-disposition".format(self.mock_server_port))
		self.assertEqual(page, b'LOLWAT?')
		self.assertEqual(fn, 'lolercoaster.txt')
		self.assertEqual(mimet, 'text/plain')

		page, fn, mimet = self.wg.getFileNameMime(
						"http://localhost:{}/filename_mime/content-disposition-html-suffix".format(self.mock_server_port))
		self.assertEqual(page, b'LOLWAT?')
		self.assertEqual(fn, 'lolercoaster.html')
		self.assertEqual(mimet, 'text/plain')

		page, fn, mimet = self.wg.getFileNameMime(
						"http://localhost:{}/filename_mime/explicit-html-mime".format(self.mock_server_port))
		self.assertEqual(page, 'LOLWAT?')
		self.assertEqual(fn, 'lolercoaster.html')
		self.assertEqual(mimet, 'text/html')

	def test_get_head(self):
		inurl_1 = "http://localhost:{}".format(self.mock_server_port)
		nurl_1 = self.wg.getHead(inurl_1)
		self.assertEqual(inurl_1, nurl_1)

		inurl_2 = "http://localhost:{}/filename_mime/content-disposition".format(self.mock_server_port)
		nurl_2 = self.wg.getHead(inurl_2)
		self.assertEqual(inurl_2, nurl_2)

	def test_redirect_handling(self):

		inurl_1 = "http://localhost:{}/redirect/from-1".format(self.mock_server_port)
		ctnt_1 = self.wg.getpage(inurl_1)
		self.assertEqual(ctnt_1, b"Redirect-To-1")

		inurl_2 = "http://localhost:{}/redirect/from-2".format(self.mock_server_port)
		ctnt_2 = self.wg.getpage(inurl_2)
		self.assertEqual(ctnt_2, b"Redirect-To-2")

		inurl_3 = "http://localhost:{}/redirect/from-1".format(self.mock_server_port)
		outurl_3 = "http://localhost:{}/redirect/to-1".format(self.mock_server_port)
		nurl_3 = self.wg.getHead(inurl_3)
		self.assertEqual(outurl_3, nurl_3)

		inurl_4 = "http://localhost:{}/redirect/from-2".format(self.mock_server_port)
		outurl_4 = "http://localhost:{}/redirect/to-2".format(self.mock_server_port)
		nurl_4 = self.wg.getHead(inurl_4)
		self.assertEqual(outurl_4, nurl_4)

		# This is a redirect without the actual redirect
		with self.assertRaises(WebRequest.FetchFailureError):
			inurl_5 = "http://localhost:{}/redirect/bad-1".format(self.mock_server_port)
			nurl_5 = self.wg.getHead(inurl_5)

		# This is a infinitely recursive redirect.
		with self.assertRaises(WebRequest.FetchFailureError):
			inurl_6 = "http://localhost:{}/redirect/bad-2".format(self.mock_server_port)
			nurl_6 = self.wg.getHead(inurl_6)

		# This is a infinitely recursive redirect.
		with self.assertRaises(WebRequest.FetchFailureError):
			inurl_6 = "http://localhost:{}/redirect/bad-3".format(self.mock_server_port)
			nurl_6 = self.wg.getHead(inurl_6)

		inurl_7 = "http://localhost:{}/redirect/from-3".format(self.mock_server_port)
		# Assumes localhost resolves to 127.0.0.1. Is this ever not true? TCPv6?
		outurl_7 = "http://127.0.0.1:{}/".format(self.mock_server_port)
		nurl_7 = self.wg.getHead(inurl_7)
		self.assertEqual(outurl_7, nurl_7)

	def test_http_auth(self):
		wg_1 = WebRequest.WebGetRobust(creds=[("localhost:{}".format(self.mock_server_port), "lol", "wat")])
		page = wg_1.getpage("http://localhost:{}/password/expect".format(self.mock_server_port))
		self.assertEqual(page, b'Password Ok?')

		wg_2 = WebRequest.WebGetRobust(creds=[("localhost:{}".format(self.mock_server_port), "lol", "nope")])
		page = wg_2.getpage("http://localhost:{}/password/expect".format(self.mock_server_port))
		self.assertEqual(page, b'Password Bad!')
