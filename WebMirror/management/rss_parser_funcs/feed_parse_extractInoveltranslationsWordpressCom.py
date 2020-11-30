def extractInoveltranslationsWordpressCom(item):
	'''
	Parser for 'inoveltranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	if item['tags'] == ['Uncategorized']:
		titlemap = [
			('Dual Life Chapter ',          'Dual Life～in day with the Hero party, in night with the Demon king Army～',      'translated'),
			('Tensei Shoujo no Rirekisho',  'Tensei Shoujo no Rirekisho',      'translated'),
			('Master of Dungeon',           'Master of Dungeon',               'oel'),
		]

		for titlecomponent, name, tl_type in titlemap:
			if titlecomponent.lower() in item['title'].lower():
				return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	tagmap = [
		('dual life',                                                                    'dual life',                                                                                   'translated'),
		('the adventure of a boy with the mind of a middle-aged man',                    'the adventure of a boy with the mind of a middle-aged man',                                   'translated'),
		('i became peerless after i threw my whole paycheck at a real-life gacha',       'i became peerless after i threw my whole paycheck at a real-life gacha',                      'translated'),
		('the falsely executed marquis\' daughter wants to live peacefully with fluffy god',       'the falsely executed marquis daughter wants to live peacefully with fluffy god',                      'translated'),
		('the falsely executed marquis daughter wants to live peacefully with fluffy god',        'the falsely executed marquis daughter wants to live peacefully with fluffy god',                       'translated'),
		('level 1 strongest sage',                                                                'level 1 strongest sage',                                                                               'translated'),
		('when the golden finger lands in the hands of the villain',                              'when the golden finger lands in the hands of the villain',                                             'translated'),
		('exiled magic swordsman',                                                                'The Exiled Jack-of-all-trades Magic Swordsman Becomes The Princess Instructor',                        'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False