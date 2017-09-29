#!/usr/bin/python3
import sys
import codecs

import http.client
import email.parser

cchardet = False

try:
	import cchardet
except ImportError:    # pragma: no cover
	pass

def isUTF8Strict(data):     # pragma: no cover - Only used when cchardet is missing.
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
		else:    # pragma: no cover
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
