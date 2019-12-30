def extract17LiterarycornerWordpressCom(item):
	'''
	Parser for '17literarycorner.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('King Of Hell\'s Genius Pampered Wife',       'King Of Hell\'s Genius Pampered Wife',                      'translated'),
		('KOH',                                        'King Of Hell\'s Genius Pampered Wife',                      'translated'),
		('Addicted to Boundlessly Pampering You',      'Addicted to Boundlessly Pampering You',                     'translated'),
		('ATBPY',                                      'Addicted to Boundlessly Pampering You',                     'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	if item['tags'] == ['Uncategorized']:
		titlemap = [
			('KOH Chapter ',                'King Of Hell\'s Genius Pampered Wife',                      'translated'),
			('Tensei Shoujo no Rirekisho',  'Tensei Shoujo no Rirekisho',      'translated'),
			('Master of Dungeon',           'Master of Dungeon',               'oel'),
		]

		for titlecomponent, name, tl_type in titlemap:
			if titlecomponent.lower() in item['title'].lower():
				return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False