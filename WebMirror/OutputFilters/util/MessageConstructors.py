

import pprint
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

def fix_string(val):
	if isinstance(val, list):
		val = [fixCase(tmp) for tmp in val]
		return val

	if not val:
		return val
	val = fixSmartQuotes(val)
	val = fixCase(val)
	val = ftfy.fix_text(val)
	return val

def fix_dict(inRelease):
	for key in inRelease.keys():
		if isinstance(inRelease[key], str):
			inRelease[key] = fix_string(inRelease[key])
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



def buildReleaseMessage(raw_item, series, vol, chap=None, frag=None, postfix='', author=None, tl_type='translated', extraData={}, matchAuthor=False):
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

	}

	# pprint.pprint(ret)

	for key, value in extraData.items():
		assert key not in ret
		ret[key] = value

	return ret


def createSeriesInfoPacket(data, beta=False, matchAuthor=False):

	expect = ['title', 'author', 'tags', 'desc', 'tl_type', 'sourcesite']
	allowed = ['alt_titles', 'author', 'desc', 'homepage', 'illust', 'pubdate', 'pubnames', 'sourcesite', 'tags', 'title', 'tl_type', 'update_only', 'coostate', 'type', 'genres', 'licensed', 'transcomplete']



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
