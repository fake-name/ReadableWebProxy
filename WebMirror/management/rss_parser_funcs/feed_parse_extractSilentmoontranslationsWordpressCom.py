def extractSilentmoontranslationsWordpressCom(item):
	'''
	Parser for 'silentmoontranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('MGCH',                        'Male God, Come Here',                        'translated'),
		('when the golden finger lands in the hands of the villain',       'when the golden finger lands in the hands of the villain',                      'translated'),
		('Rare Treasure',               'Rare Treasure',                              'translated'),
		('Ostentatious Zhao Yao',       'Ostentatious Zhao Yao',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False