



def buildReleaseMessage(raw_item, series, vol, chap=None, frag=None, postfix='', author=None, tl_type='translated', extraData={}):
	'''
	Special case behaviour:
		If vol or chapter is None, the
		item in question will sort to the end of
		the relevant sort segment.
	'''
	ret = {
		'srcname'   : raw_item['srcname'],
		'series'    : series,
		'vol'       : vol,
		'chp'       : packChapterFragments(chap, frag),
		'published' : raw_item['published'],
		'itemurl'   : raw_item['linkUrl'],
		'postfix'   : postfix,
		'author'    : author,
		'tl_type'   : tl_type,
	}

	for key, value in extraData.items():
		assert key not in ret
		ret[key] = value
	return ret

def packChapterFragments(chapStr, fragStr):
	if not chapStr and not fragStr:
		return None
	if not fragStr:
		return chapStr

	# Handle cases where the fragment is present,
	# but the chapStr is None
	if chapStr == None:
		chapStr = 0

	chap = float(chapStr)
	frag = float(fragStr)
	return '%0.2f' % (chap + (frag / 100.0))
