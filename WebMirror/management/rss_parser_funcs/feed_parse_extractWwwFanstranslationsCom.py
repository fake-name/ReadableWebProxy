def extractWwwFanstranslationsCom(item):
	'''
	Parser for 'www.fanstranslations.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('i help the richest man spend money to prevent disasters',       'i help the richest man spend money to prevent disasters',                      'translated'),
		('the widow "misses" her villainous late husband',                'the widow "misses" her villainous late husband',                               'translated'),
		('endless plunder in high school dxd',                            'endless plunder in high school dxd',                                           'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False