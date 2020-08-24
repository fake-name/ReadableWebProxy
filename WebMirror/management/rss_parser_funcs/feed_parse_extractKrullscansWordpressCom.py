def extractKrullscansWordpressCom(item):
	'''
	Parser for 'krullscans.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('oi, hazure sukiruda to omowareteita "chiito koodo soosa" ga bakemono sugirandaga',       'oi, hazure sukiruda to omowareteita "chiito koodo soosa" ga bakemono sugirandaga',                      'translated'),
		('i was summoned to a parallel fantasy world for too many times',       'i was summoned to a parallel fantasy world for too many times',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False