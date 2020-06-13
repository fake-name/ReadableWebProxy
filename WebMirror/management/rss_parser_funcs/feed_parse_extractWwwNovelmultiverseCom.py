def extractWwwNovelmultiverseCom(item):
	'''
	Parser for 'www.novelmultiverse.com'
	'''


	badwords = [
			'VIP',
			'badword',
		]
	if any([bad in item['tags'] for bad in badwords]):
		return None



	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None


	if item['tags'] == []:
		titlemap = [
			('Heaven Awakening Path',                             'Heaven Awakening Path',                                 'translated'),
			('Master of Science and Technology',                  'Master of Science and Technology',                      'translated'),
			('Reincarnated Young Lady Aims to Be an Adventurer',  'Reincarnated Young Lady Aims to Be an Adventurer',      'translated'),
			('Don’t Turn from Summer',                            'Don’t Turn from Summer',                                'translated'),
			('The Girl Who Spits Up Jewels - Volume ',  'The Girl Who Spits Up Jewels',      'translated'),
			('Tensei Shoujo no Rirekisho',  'Tensei Shoujo no Rirekisho',      'translated'),
			('Master of Dungeon',           'Master of Dungeon',               'oel'),
		]

		for titlecomponent, name, tl_type in titlemap:
			if titlecomponent.lower() in item['title'].lower():
				return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	tagmap = [
		('elememtaryharem',                                         'After returning to elementary school with my memory the result was to create a harem',   'translated'),
		('elementaryharem',                                         'After returning to elementary school with my memory the result was to create a harem',   'translated'),
		('Parameter remote controller',                             'Parameter remote controller',                                                            'translated'),
		('auto assigned villainess',                                'auto assigned villainess',                                                               'translated'),
		('the reincarnated young lady aims to be an adventurer',    'the reincarnated young lady aims to be an adventurer',                                   'translated'),
		('the daily life of the fairy king',                        'the daily life of the fairy king',                                       'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False