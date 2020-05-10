def extractSleepytranslationsCom(item):
	'''
	Parser for 'sleepytranslations.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	if item['tags'] == ['Uncategorized']:
		titlemap = [
			('What is My Brother is Too Good? Chapter ',                  'What if My Brother is Too Good?',                      'translated'),
			('What if My Brother is Too Good? Chapter ',                  'What if My Brother is Too Good?',                      'translated'),
			('I Became the Villain’s Pendant Chapter ',                   'I Became the Villain’s Pendant',                       'translated'),
			('Rebirth of the Film Emperor’s Beloved Wife Chapter ',       'Rebirth of the Film Emperor’s Beloved Wife',           'translated'),
			('Our Binding Love: My Gentle Tyrant Chapter ',               'Our Binding Love: My Gentle Tyrant',                   'translated'),
			('Film Emperor’s Adorable Wife From Ancient Times Chapter ',  'Film Emperor’s Adorable Wife From Ancient Times',      'translated'),
			('My Big Brother is Seeking Death Again Chapter ',            'My Big Brother is Seeking Death Again',                'translated'),
			('Great God, I’ll Support You Chapter ',                      'Great God, I’ll Support You',                          'translated'),
			('Quick Transmigration: Snatching Golden Fingers Chapter ',   'Quick Transmigration: Snatching Golden Fingers',       'translated'),
			('Tensei Shoujo no Rirekisho',  'Tensei Shoujo no Rirekisho',      'translated'),
			('Master of Dungeon',           'Master of Dungeon',               'oel'),
		]

		for titlecomponent, name, tl_type in titlemap:
			if titlecomponent.lower() in item['title'].lower():
				return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	tagmap = [
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False