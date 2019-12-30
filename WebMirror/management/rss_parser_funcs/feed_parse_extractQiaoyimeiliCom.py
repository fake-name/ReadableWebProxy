def extractQiaoyimeiliCom(item):
	'''
	Parser for 'qiaoyimeili.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Rebirth of Gu Jiao',                 'Rebirth of Gu Jiao',                                'translated'),
		('Wang Ye is a Demon',                 'Wang Ye is a Demon',                                'translated'),
		('why are you doing this, duke!',      'Why Are You Doing This Duke!',                      'translated'),
		('Why Are You Doing This Duke!',       'Why Are You Doing This Duke!',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	if item['tags'] == ['Deanie\'s Corner']:
		titlemap = [
			('The Innocent Young Master Lu – Chapter ',  'The Innocent Young Master Lu',       'translated'),
			('Why Are You Doing This, Duke! Vol. ',      'Why Are You Doing This, Duke!',      'translated'),
			('Tensei Shoujo no Rirekisho',  'Tensei Shoujo no Rirekisho',      'translated'),
			('Master of Dungeon',           'Master of Dungeon',               'oel'),
		]

		for titlecomponent, name, tl_type in titlemap:
			if titlecomponent.lower() in item['title'].lower():
				return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False