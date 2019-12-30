def extractTenshihonyakushaWordpressCom(item):
	'''
	Parser for 'tenshihonyakusha.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Power in the Shadows',       'To Be a Power in the Shadows!',                                                                             'translated'),
		('Megami Buchigire',           'Megami Buchigire',                                                                                          'translated'),
		('MotoKimama',                 'The Oppressed Savior Abandons The Other World to Live As He Pleases in His Own World',                      'translated'),
		('OreMegane',                  'Ore no Megane wa Tabun Sekai Seifuku dekiru to Omou.',                                                      'translated'),
		('SecretOrg',                  'There Was No Secret Organization to Fight with the World’s Darkness so I Made One (In Exasperation)',       'translated'),
		('TRPG',                       'The Wizard Raised Through TRPG is Still the Strongest in the Other World',                                  'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)
	
	if item['tags'] == [] or item['tags'] == ['Uncategorized']:
		titlemap = [
			('MayoJou Ch ',                 'The Chronicles of a Lost Man in His Forties Founding a Nation ~Commonsense is Hindering Me From Becoming TUEE~',      'translated'),
			('Power in the Shadows',        'To Be a Power in the Shadows!',                                                                                       'translated'),
			('Tensei Shoujo no Rirekisho',  'Tensei Shoujo no Rirekisho',      'translated'),
			('Master of Dungeon',           'Master of Dungeon',               'oel'),
		]

		for titlecomponent, name, tl_type in titlemap:
			if titlecomponent.lower() in item['title'].lower():
				return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



	return False