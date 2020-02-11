def extractAveragecatWordpressCom(item):
	'''
	Parser for 'averagecat.wordpress.com'
	Parser for 'raisingmytail.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('PRC',       'PRC',                      'translated'),
			('mitsuha',  'Rougo ni Sonaete Isekai de 8-manmai no Kinka wo Tamemasu',      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)
	
	if item['tags'] == ['Uncategorized']:
		titlemap = [
			('Mitsuha ',  'Rougo ni Sonaete Isekai de 8-manmai no Kinka wo Tamemasu',      'translated'),
			('Master of Dungeon',           'Master of Dungeon',               'oel'),
		]

		for titlecomponent, name, tl_type in titlemap:
			if titlecomponent.lower() in item['title'].lower():
				return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False