def extractBrotakusCom(item):
	'''
	Parser for 'brotakus.com'
	'''
	if 'Anime' in item['tags']:
		return None
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('gakusen toshi asterisk',         'Gakusen Toshi Asterisk',                        'translated'),
		('I Shall Seal the Heavens',       'I Shall Seal the Heavens',                      'translated'),
		('ISSTH',                          'I Shall Seal the Heavens',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False