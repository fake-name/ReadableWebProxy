def extractTranslatingboredomWordpressCom(item):
	'''
	Parser for 'translatingboredom.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('rcfn chapters',       'Rebirth of a Cannon Fodder in a Novel',                      'translated'),
		('rcfn',                'Rebirth of a Cannon Fodder in a Novel',                      'translated'),
		('mhsc chapters',       'Me and my Husband Sleep in a Coffin',                      'translated'),
		('mhsc',                'Me and my Husband Sleep in a Coffin',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False