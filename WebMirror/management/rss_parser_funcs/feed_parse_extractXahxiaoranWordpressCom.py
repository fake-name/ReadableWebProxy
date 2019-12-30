def extractXahxiaoranWordpressCom(item):
	'''
	Parser for 'xahxiaoran.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	titlemap = [
		('IWUPWAJC ',                                           'I Woke Up Pregnant With An Undead\'s Child',          'translated'),
		('I Woke Up Pregnant With An Undead’s Child Chapter ',  'I Woke Up Pregnant With An Undead\'s Child',          'translated'),
		('The Rich And Powerful Chang An Chapter ',             'The Rich And Powerful Chang An',                      'translated'),
		('TRAPC ',                                              'The Rich And Powerful Chang An',                      'translated'),
		('TRAHC ',                                              'The Rich And Powerful Chang An',                      'translated'),
		('Master of Dungeon',           'Master of Dungeon',               'oel'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	if item['tags'] == ['translation']:
		titlemap = [
			('Exile Chapter ',              'Exile [Farming]',                     'translated'),
			('TRAHPC Chapter ',             'The Rich And Honorable ChangAn',      'translated'),
			('Tensei Shoujo no Rirekisho',  'Tensei Shoujo no Rirekisho',      'translated'),
			('Master of Dungeon',           'Master of Dungeon',               'oel'),
		]

		for titlecomponent, name, tl_type in titlemap:
			if titlecomponent.lower() in item['title'].lower():
				return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False