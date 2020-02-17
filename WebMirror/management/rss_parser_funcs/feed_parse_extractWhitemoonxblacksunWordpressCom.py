def extractWhitemoonxblacksunWordpressCom(item):
	'''
	Parser for 'whitemoonxblacksun.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('i have paid too much for this home',                 'i have paid too much for this home',                                'translated'),
		('Reborn Otaku Code of Practice for Apocalypse',       'Reborn Otaku Code of Practice for Apocalypse',                      'translated'),
		('Jumpchain',                                          'Jump Chain',                                                        'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False