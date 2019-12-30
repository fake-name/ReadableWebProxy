def extractMobofdeerWordpressCom(item):
	'''
	Parser for 'mobofdeer.wordpress.com'
	'''
	
	if '(manga)' in item['title']:
		return None
	
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Summoning Japan',       'Summoning Japan',                                        'translated'),
		('MaouSaikon',            'The Demon Lord\'s Second Marriage',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False