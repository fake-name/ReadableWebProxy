def extractTotallytranslationsCom(item):
	'''
	Parser for 'totallytranslations.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Peerless Martial God',       'Peerless Martial God',                      'translated'),
		('Heavenly Curse',             'Heavenly Curse',                            'translated'),
		('Devouring The Heavens',      'Devouring The Heavens',                     'translated'),
		('Peerless Martial God 2',     'Peerless Martial God 2',                    'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False