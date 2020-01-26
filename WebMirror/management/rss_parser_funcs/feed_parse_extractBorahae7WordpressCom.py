def extractBorahae7WordpressCom(item):
	'''
	Parser for 'borahae7.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Prophet',       'The Strongest Prophet Who Had Trained 100 Heroes is Admired By His Apprentices Around The World Even As An Adventurer',                      'translated'),
		('fbcbtr',          'Fiancee Be Chosen By The Ring',      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	if item['tags'] == ['Uncategorized']:
		titlemap = [
			('FIANCEE BE CHOSEN BY THE RING — CHAPTER ',          'Fiancee Be Chosen By The Ring',      'translated'),
			('THE STRONGEST PROPHET — CH',                        'The Strongest Prophet Who Has Trained 100 Heroes is Admired By His Apprentices Around The World Even As An Adventurer',         'translated'),
			('Tensei Shoujo no Rirekisho',                        'Tensei Shoujo no Rirekisho',         'translated'),
			('Master of Dungeon',                                 'Master of Dungeon',                  'oel'),
		]

		for titlecomponent, name, tl_type in titlemap:
			if titlecomponent.lower() in item['title'].lower():
				return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



	return False