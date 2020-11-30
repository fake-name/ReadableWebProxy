def extractThestrangeobserversWordpressCom(item):
	'''
	Parser for 'thestrangeobservers.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('sign in',                      'sign in',                          'translated'),
		('bei hai zoo',                  'bei hai zoo',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	titlemap = [
		('House Dad’s Literary Life c',  'House Dad’s Literary Life',        'translated'),
		('Rebirth In A Perfect Era',     'Rebirth In A Perfect Era',         'translated'),
		('Tensei Shoujo no Rirekisho',   'Tensei Shoujo no Rirekisho',       'translated'),
		('I made the world mutate',      'I made the world mutate',          'translated'),
		('Master of Dungeon',            'Master of Dungeon',                'oel'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False