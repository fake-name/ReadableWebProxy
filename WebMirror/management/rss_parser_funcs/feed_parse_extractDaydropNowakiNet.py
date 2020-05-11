def extractDaydropNowakiNet(item):
	'''
	Parser for 'daydrop.nowaki.net'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Yes, No, or Maybe Half?',       'Yes, No, or Maybe Half?',                                                   'translated'),
		('bloodlines ablaze',             'bloodlines ablaze',                                                         'translated'),
		('side profiles and irises',      'Side Profiles and Irises ~Yes, No, or Maybe Half? Spinoff~',                'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False