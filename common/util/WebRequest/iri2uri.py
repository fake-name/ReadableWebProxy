
import urllib.parse

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
