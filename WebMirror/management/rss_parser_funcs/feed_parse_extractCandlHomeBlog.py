def extractCandlHomeBlog(item):
	'''
	Parser for 'candl.home.blog'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('zombie master',                                                                                   'Zombie Master',                                                                                                  'translated'),
		('Because I Was Excluded Out of the Class Transfer, I Decided to Steal My Classmate’s Lover',       'Because I Was Excluded Out of the Class Transfer, I Decided to Steal My Classmate\'s Lover',                     'translated'),
		('OTOTSUKAI WA SHI TO ODORU',                                                                       'Ototsukai wa Shi to Odoru',                                                                                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False