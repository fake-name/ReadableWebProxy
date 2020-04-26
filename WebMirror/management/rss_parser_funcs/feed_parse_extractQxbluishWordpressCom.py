def extractQxbluishWordpressCom(item):
	'''
	Parser for 'qxbluish.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	titlemap = [
		('Golden Age of Phoenix: TFCVIC',  'Golden Age of Phoenix: Tyrant’s First Class Virtuous Imperial Concubine',      'translated'),
		('MDWMSEIPL: Chapter ',            'My Daughter Was My Sworn Enemy In Past Life',                                  'translated'),
		('Master of Dungeon',           'Master of Dungeon',               'oel'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	tagmap = [
		('tyrants',       'Golden Age of Phoenix: Tyrant\'s First Class Virtuous Imperial Concubine',                      'translated'),
		('tfwoiwm',       'The Former Wife of Invisible Wealthy Man',                                                      'translated'),
		('fanshu',        'Crossing Into The Emperor’s Body At Night',                                                     'translated'),
		('mdwmseipl',     'My Daughter Was My Sworn Enemy In Past Life',                                                   'translated'),
		('tpmofbs',       'Transmigration: Petite Mother Of Four Big Shots',                                               'translated'),
		('bhwatp',        'Become Husband and Wife According To Pleasure',                                                 'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False