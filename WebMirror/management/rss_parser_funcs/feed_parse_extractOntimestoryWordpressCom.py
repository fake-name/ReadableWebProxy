def extractOntimestoryWordpressCom(item):
	'''
	Parser for 'ontimestory.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
	
	if chp == 2019:
		return None
	
	badwords = [
			'Dark Blue Kiss',
			'2moons2',
			'2Moons2',
			'Love By Chance',
			'Love by Chance',
			'Theory of Love',
		]
	if any([bad in item['title'] for bad in badwords]):
		return None


	
				

	if item['tags'] == ['Bez kategorii']:
		
		titlemap = [
			('My Artist is Reborn – Chapter ',             'My Artist is Reborn',             'translated'),
			('MAIR – Chapter ',             'My Artist is Reborn',             'translated'),
			('TOFUH – Chapter ',            'The only favourite ugly husband', 'translated'),
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