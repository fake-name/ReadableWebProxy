def extractRanobekaWordpressCom(item):
	'''
	Parser for 'ranobeka.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('IAP',       'I was caught up in a Hero Summoning, but that World is at Peace',                    'translated'),
		('DM',        'Dungeon Master',                                                                     'translated'),
		('TWBFOM',    'The world became full of monsters, so I guessed I should live how I want to',        'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False