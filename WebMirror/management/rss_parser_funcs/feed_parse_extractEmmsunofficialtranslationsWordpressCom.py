def extractEmmsunofficialtranslationsWordpressCom(item):
	'''
	Parser for 'emmsunofficialtranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	if item['tags'] == ['Uncategorized'] or item['tags'] == ['Novel'] or item['tags'] == ['Chinese Novel']:
		titlemap = [
			('Rebirth of a Star General: Chapter ',  'Rebirth of a Star General',      'translated'),
			('Rebirth of a Star General (Chapter ',  'Rebirth of a Star General',      'translated'),
			('Crimson Karma: Chapter ',  'Crimson Karma ',      'translated'),
			('My Lady, Please Become My Heroine!: Chapter ',  'My Lady, Please Become My Heroine!',      'translated'),
			('Tensei Shoujo no Rirekisho',  'Tensei Shoujo no Rirekisho',      'translated'),
			('Master of Dungeon',           'Master of Dungeon',               'oel'),
		]

		for titlecomponent, name, tl_type in titlemap:
			if titlecomponent.lower() in item['title'].lower():
				return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	tagmap = [
		('feng xing',       'feng xing',                      'translated'),
		('rebirth of a star general',  'Rebirth of a Star General',      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False