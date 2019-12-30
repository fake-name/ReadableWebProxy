def extract2Slow2LatemtlWordpressCom(item):
	'''
	Parser for '2slow2latemtl.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('HP1 kara Hajimeru Isekai Musou',                                'HP1 kara Hajimeru Isekai Musou',                                               'translated'),
		("A Loner With The Trash Skill 'Abnormal Status Doubling'",       "A Loner With The Trash Skill 'Abnormal Status Doubling'",                      'translated'),
		('Is it Tough Being a Friend?',                                   'Is it Tough Being a Friend?',                                                  'translated'),
		('Lonely Attack on the Different World',                          'Lonely Attack on the Different World',                                         'translated'),
		('The World of Otome Games is Tough for Mobs',                    'The World of Otome Games is Tough for Mobs',                                   'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False