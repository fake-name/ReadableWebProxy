def extractPigcowTranslationsCom(item):
	'''
	Parser for 'pigcow-translations.com'
	'''
	badwords = [
			'Learn Japanese',
			'Learn Japanese Level 1',
			'Interviews',
		]
	if any([bad in item['tags'] for bad in badwords]):
		return None

	titlestr = item['title'] + " ".join(item['tags'])

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(titlestr)
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Seven Wonders Overtime',       'Seven Wonders Overtime',               'translated'),
		('holmes of kyoto',              'Holmes of Kyoto',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False