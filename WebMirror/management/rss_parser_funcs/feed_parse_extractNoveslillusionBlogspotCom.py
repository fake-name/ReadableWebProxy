def extractNoveslillusionBlogspotCom(item):
	'''
	Parser for 'noveslillusion.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	if item['tags'] == ['Chapter'] or item['tags'] == []:
		titlemap = [
			('I\'m the Evil Lord of an Intergalactic Empire! Chapter',  'I’m the Evil Lord of an Intergalactic Empire! Chapter',      'translated'),
			('I\'m the Evil Lord of an Intergalactic Empire Chapter',  'I’m the Evil Lord of an Intergalactic Empire! Chapter',      'translated'),
			('I’m the Evil Lord of an Intergalactic Empire! Chapter',  'I’m the Evil Lord of an Intergalactic Empire! Chapter',      'translated'),
			('The rat boy survives the apocalypse',  'The rat boy survives the apocalypse',      'translated'),
			('Reincarnated as the villainous pig orc duke',  'Reincarnated as the villainous Duke Orc Pig',      'translated'),
			('Reincarnated as the villainous Duke Orc Pig',  'Reincarnated as the villainous Duke Orc Pig',      'translated'),
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