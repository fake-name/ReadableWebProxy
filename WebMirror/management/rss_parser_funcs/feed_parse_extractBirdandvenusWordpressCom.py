def extractBirdandvenusWordpressCom(item):
	'''
	Parser for 'birdandvenus.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
		

	titlemap = [
		('TCFO c.',       'The Transmigrated Cannon Fodder Overthrows the Male Protagonist',                      'translated'),
		('TUD c.',        'The Unfulfilled Desire',                                                               'translated'),
		('Master of Dungeon',           'Master of Dungeon',               'oel'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	return False