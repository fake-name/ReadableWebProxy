def extractAshenfeatherWordpressCom(item):
	'''
	Parser for 'ashenfeather.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Sweet Curse! Battle-Android summoned to a Different world!',       'Sweet Curse! Battle-Android summoned to a Different world!',                      'translated'),
		('She was called God, as well as Satan',                             'She was called God, as well as Satan',                                            'translated'),
		('She was Called Both God & Satan',                                  'She was called God, as well as Satan',                                            'translated'),
		('At the Northern Fort',                                             'At the Northern Fort',                                                            'translated'),
		('Girl with the Golden-Cat Eyes',                                    'Girl with the Golden-Cat Eyes',                                                   'oel'),
		('One in the Chamber',                                               'One in the Chamber',                                                              'oel'),
		('Parabellum',                                                       'Parabellum',                                                                      'oel'),
		('Sky Gardens',                                                      'Sky Gardens',                                                                     'oel'),
		('Manuke FPS',                                                       'Manuke FPS',                                                                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)
	if item['tags'] == ['Uncategorized']:
		titlemap = [
			('Flowered Metal | ',           'Flowered Metal',                  'translated'),
			('Master of Dungeon',           'Master of Dungeon',               'oel'),
		]

		for titlecomponent, name, tl_type in titlemap:
			if titlecomponent.lower() in item['title'].lower():
				return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False