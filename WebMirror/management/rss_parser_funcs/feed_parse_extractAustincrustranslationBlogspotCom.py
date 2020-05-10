def extractAustincrustranslationBlogspotCom(item):
	'''
	Parser for 'austincrustranslation.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	if item['tags'] == []:
		titlemap = [
			('Isekai de Slow Life wo (Ganbou) Chapter ',  'Isekai de Slow Life wo (Ganbou)',      'translated'),
			('Isekai De Slow Live wo (Ganbou) Chapter ',  'Isekai de Slow Life wo (Ganbou)',      'translated'),
			('Isekai de Slow Life wo (Ganbou} Chapter ',  'Isekai de Slow Life wo (Ganbou)',      'translated'),
			('Tensei Shoujo no Rirekisho',  'Tensei Shoujo no Rirekisho',      'translated'),
			('Master of Dungeon',           'Master of Dungeon',               'oel'),
		]

		for titlecomponent, name, tl_type in titlemap:
			if titlecomponent.lower() in item['title'].lower():
				return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	tagmap = [
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False