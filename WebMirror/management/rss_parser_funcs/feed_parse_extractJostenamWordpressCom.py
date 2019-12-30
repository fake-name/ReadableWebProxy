def extractJostenamWordpressCom(item):
	'''
	Parser for 'jostenam.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('MCEA',       'My Cherry Will Explode in the Apocalypse',                       'translated'),
		('TEWRCFC',    'The End of The World’s Reborn Cannon Fodder Counter-attacks',    'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False