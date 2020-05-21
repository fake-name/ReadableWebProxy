def extractLiplilyBlogspotCom(item):
	'''
	Parser for 'liplily.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	if item['tags'] == []:
		titlemap = [
			('The Farmer Girl Gets Rich',                                    'The Farmer Girl Gets Rich',                               'translated'),
			('Invincible Baby Mommy : Chapter ',                             'Invincible Baby Mommy',                                   'translated'),
			('Invincible baby mommy :Chapter ',                              'Invincible Baby Mommy',                                   'translated'),
			('The strongest little devil: Master, come to fight! Chapter ',  'The strongest little devil: Master, come to fight!',      'translated'),
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