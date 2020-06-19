def extractJustatranslatortranslationsCom(item):
	'''
	Parser for 'justatranslatortranslations.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('legend of the great sage',       'legend of the great sage',                      'translated'),
		('lgs',                            'legend of the great sage',                      'translated'),
		('CSG',                            'Chaotic Sword God',                             'translated'),
		('Chaotic Sword God',              'Chaotic Sword God',                             'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	if item['tags'] == ['Uncategorized']:
		titlemap = [
			('A Sword Through the Nine Heavens',   'A Sword Through the Nine Heavens',      'translated'),
			('Chaotic Sword God',                  'Chaotic Sword God',                     'translated'),
			('Legend of the Great Sage Chapter ',  'Legend of the Great Sage',              'translated'),
			('Tensei Shoujo no Rirekisho',  'Tensei Shoujo no Rirekisho',      'translated'),
			('Master of Dungeon',           'Master of Dungeon',               'oel'),
		]

		for titlecomponent, name, tl_type in titlemap:
			if titlecomponent.lower() in item['title'].lower():
				return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False