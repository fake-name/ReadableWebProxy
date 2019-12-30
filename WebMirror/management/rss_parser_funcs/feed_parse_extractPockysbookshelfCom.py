def extractPockysbookshelfCom(item):
	'''
	Parser for 'pockysbookshelf.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('I Tamed a Tyrant and Ran Away',                                           'I Tamed a Tyrant and Ran Away',                                     'translated'),
		('If I Happened to Tame my Brother Well',                                   'If I Happened to Tame my Brother Well',                             'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	if item['tags'] == [] or item['tags'] == ['novels']:
		titlemap = [
			('I Tamed a Tyrant and Ran Away: Chapter ',                                 'I Tamed a Tyrant and Ran Away',                                     'translated'),
			('Methods to Save the Villain who was Abandoned by the Heroine: Chapter ',  'Methods to Save the Villain who was Abandoned by the Heroine',      'translated'),
			('First of All, Let’s Hide My Younger Brother: Chapter ',                   'First of All, Let’s Hide My Younger Brother',                       'translated'),
			('The End of this Fairy Tale is One Hell of a Drama: Chapter ',             'The End of this Fairy Tale is One Hell of a Drama',                 'translated'),
			('If I Happened to Tame my Brother Well',                                   'If I Happened to Tame my Brother Well',                             'translated'),
			('Tensei Shoujo no Rirekisho',  'Tensei Shoujo no Rirekisho',      'translated'),
			('Master of Dungeon',           'Master of Dungeon',               'oel'),
		]

		for titlecomponent, name, tl_type in titlemap:
			if titlecomponent.lower() in item['title'].lower():
				return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False