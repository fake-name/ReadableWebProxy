

import pprint
import unicodedata
import sys
import re
import json
import ftfy


def fixSmartQuotes(text):
	if isinstance(text, list):
		text = [fixSmartQuotes(tmp) for tmp in text]
		return text
	text = text.replace(r"\'", "'")
	text = text.replace(r'\"', '"')
	text = text.replace(r"’", "'")
	text = text.replace(r"‘", "'")
	text = text.replace(r"“", '"')
	text = text.replace(r"”", '"')
	return text

def fixCase(inText):
	if isinstance(inText, list):
		inText = [fixCase(tmp) for tmp in inText]
		return inText
	caps  = sum(1 for c in inText if c.isupper())
	lower = sum(1 for c in inText if c.islower())
	if (lower == 0) or (caps == 0) or (caps / lower) > 2.5:
		inText = inText.title()
	return inText

WHITESPACE_CHARS = [
		'\t', '\n', '\x0b', '\x0c', '\r', '\x1c', '\x1d', '\x1e', '\x1f', ' ',
		'\x85', '\xa0', '\u1680', '\u2000', '\u2001', '\u2002', '\u2003',
		'\u2004', '\u2005', '\u2006', '\u2007', '\u2008', '\u2009', '\u200a',
		'\u2028', '\u2029', '\u202f', '\u205f', '\u3000'
	]
def fixHtmlEntities(inText):
	inText = inText.replace('&nbsp;', ' ')
	inText = inText.replace('&lt;', '<')
	inText = inText.replace('&gt;', '>')
	inText = inText.replace('&amp;', '&')
	inText = inText.replace('&quot;', '"')
	inText = inText.replace('&apos;', '\'')
	inText = inText.replace('&cent;', '¢')
	inText = inText.replace('&pound;', '£')
	inText = inText.replace('&yen;', '¥')
	inText = inText.replace('&euro;', '€')
	inText = inText.replace('&copy;', '©')
	inText = inText.replace('&reg;', '®')
	inText = inText.replace('&#160;', ' ')
	inText = inText.replace('&#60;', '<')
	inText = inText.replace('&#62;', '>')
	inText = inText.replace('&#38;', '&')
	inText = inText.replace('&#34;', '"')
	inText = inText.replace('&#39;', '\'')
	inText = inText.replace('&#162;', '¢')
	inText = inText.replace('&#163;', '£')
	inText = inText.replace('&#165;', '¥')
	inText = inText.replace('&#8364;', '€')
	inText = inText.replace('&#169;', '©')
	inText = inText.replace('&#174;', '®')
	return inText

def fixUnicodeSpaces(val):
	for badchar in WHITESPACE_CHARS:
		val = val.replace(badchar, " ")
	while "  " in val:
		val = val.replace("  ", " ")
	return val

def fix_string(val):
	if isinstance(val, list):
		val = [fixCase(tmp) for tmp in val]
		return val

	if not val:
		return val
	val = fixUnicodeSpaces(val)
	val = fixSmartQuotes(val)
	val = fixCase(val)
	val = fixHtmlEntities(val)
	val = ftfy.fix_text(val)
	return val

def fix_dict(inRelease):
	for key in inRelease.keys():
		if isinstance(inRelease[key], str):
			inRelease[key] = fix_string(inRelease[key])

	# Managed to derp this somehow.
	if 'tl_type' in inRelease:
		inRelease["tl_type"] = inRelease["tl_type"].lower()

	return inRelease


def pack_message(type, data, is_beta=False):

	ret = {
		'type' : type,
		'data' : data,

		# "beta" items are optionally filtered client-end to allow
		# testing in my dev env without having the feed outputs go through
		# to the prod env
		'beta'      : is_beta,
	}
	return json.dumps(ret).encode("utf-8")



def buildReleaseMessage(raw_item,
						series,
						vol,
						chap=None,
						frag=None,
						postfix='',
						author=None,
						tl_type='translated',
						extraData={},
						matchAuthor=False,
						looseMatch=False):
	'''
	Special case behaviour:
		If vol or chapter is None, the
		item in question will sort to the end of
		the relevant sort segment.
	'''

	ret = {
		'srcname'      : raw_item['srcname'],
		'series'       : fix_string(series),
		'vol'          : vol,
		'chp'          : chap,
		'frag'         : frag,
		'published'    : raw_item['published'],
		'itemurl'      : raw_item['linkUrl'],
		'postfix'      : fix_string(postfix),
		'author'       : fix_string(author),
		'tl_type'      : tl_type,
		'match_author' : matchAuthor,
		'loose_match'  : looseMatch,

	}

	# pprint.pprint(ret)

	for key, value in extraData.items():
		assert key not in ret
		ret[key] = value

	return ret


def createSeriesInfoPacket(data, beta=False, matchAuthor=False):

	expect = ['title', 'author', 'tags', 'desc', 'tl_type', 'sourcesite']
	allowed = [
		'alt_titles',
		'author',
		'desc',
		'homepage',
		'illust',
		'pubdate',
		'pubnames',
		'sourcesite',
		'tags',
		'title',
		'tl_type',
		'update_only',
		'coostate',
		'type',
		'genres',
		'licensed',
		'transcomplete',
		'create_tags',
	]



	# assert len(expect) == len(data),             "Invalid number of items in metadata packet! Expected: '%s', received '%s'" % (expect, data)
	assert all([key in data for key in expect]), "Invalid key in metadata message! Expect: '%s', received '%s'" % (expect, list(data.keys()))

	haven = list(data.keys())
	[haven.remove(tmp) for tmp in allowed if tmp in haven]
	assert len(haven) == 0, "Disallowed tag in update! Uncleared tags: '%s'" % haven

	data['title']        = fix_string(data['title'])
	data['desc']         = fix_string(data['desc'])
	data['match_author'] = matchAuthor

	return pack_message('series-metadata', data, is_beta=beta)


def createReleasePacket(data, beta=False):
	'''
	Release packets can have "extra" data, so just check it's long enough and we have the keys we expect.	'''

	expect = ['srcname', 'series', 'vol', 'chp', 'published', 'itemurl', 'postfix', 'author', 'tl_type']

	assert len(expect) <= len(data), "Invalid number of items in release packet! Expected: '%s', received '%s'" % (expect, data)
	assert all([key in data for key in expect]), "Invalid key in release message! Expect: '%s', received '%s'" % (expect, list(data.keys()))

	data['series']  = fix_string(data['series'])
	data['postfix'] = fix_string(data['postfix'])
	data['author']  = fix_string(data['author'])

	return pack_message('parsed-release', data, is_beta=beta)
