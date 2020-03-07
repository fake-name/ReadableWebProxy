def extractNastriumdenBlogspotCom(item):
	'''
	Parser for 'nastriumden.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('The Jade Emperor Heaven Imperial Court Kindergarten',       'The Jade Emperor Heaven Imperial Court Kindergarten',                      'translated'),
		('Rebirth of The Golden Marriage',                            'Rebirth of The Golden Marriage',                                           'translated'),
		('Banished to Another World',                                 'Banished to Another World',                                                'translated'),
		('You\'re In Love With An Idiot',                             'You\'re In Love With An Idiot',                                            'translated'),
		('Years of Intoxication.',                                    'Years of Intoxication.',                                                   'translated'),
		('Blood Contract',                                            'Blood Contract',                                                           'translated'),
		('Number One Zombie Wife',                                    'Number One Zombie Wife',                                                   'translated'),
		('True Star',                                                 'True Star',                                                                'translated'),
		('s.c.i mystery',                                             'S.C.I Mystery Series',                                                     'translated'),
		('tharntype the series',       'tharntype the series',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	titlemap = [
		('The Ugly Empress vol ',       'The Ugly Empress',      'translated'),
		('The Ugly Empress, Chapter ',  'The Ugly Empress',      'translated'),
		('Blood Contract, Chapter ',    'Blood Contract',        'translated'),
		('Tensei Shoujo no Rirekisho',  'Tensei Shoujo no Rirekisho',      'translated'),
		('Master of Dungeon',           'Master of Dungeon',               'oel'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False