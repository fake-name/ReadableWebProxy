def extractWwwFringeoctopusCom(item):
	'''
	Parser for 'www.fringeoctopus.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('TWQQF',                                            'Transmigration with QQ Farm',                                                'translated'),
		('Black Belly Wife',                                 'Black Belly Wife',                                                           'translated'),
		('BBW',                                              'Black Belly Wife',                                                           'translated'),
		('Transmigrating with a Cleaver',                    'Transmigrating with a Cleaver',                                              'translated'),
		('resplendent farming apothecary',                   'resplendent farming apothecary',                                             'translated'),
		('PRC',                                              'PRC',                                                                        'translated'),
		('Loiterous',                                        'Loiterous',                                                                  'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False