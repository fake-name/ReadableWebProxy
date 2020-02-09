def extractSumtlmanCom(item):
	'''
	Parser for 'sumtlman.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	if item['tags'] == ['Update']:
		titlemap = [
			('Super Dimensional Wizard Ch.',       'Super Dimensional Wizard',        'translated'),
			('SDW Ch. ',                           'Super Dimensional Wizard',        'translated'),
			('Tensei Shoujo no Rirekisho',         'Tensei Shoujo no Rirekisho',      'translated'),
			('MDT Ch. ',                           'My Doomsday Territory',           'translated'),
			('EC Ch. ',                            'Eternal Country',                 'translated'),
			('Master of Dungeon',                  'Master of Dungeon',               'oel'),
		]

		for titlecomponent, name, tl_type in titlemap:
			if titlecomponent.lower() in item['title'].lower():
				return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	return False