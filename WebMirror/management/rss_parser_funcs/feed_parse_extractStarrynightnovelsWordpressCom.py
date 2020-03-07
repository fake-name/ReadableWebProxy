def extractStarrynightnovelsWordpressCom(item):
	'''
	Parser for 'starrynightnovels.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Shini Yasui Kōshaku Reijō to Shichi-nin no Kikōshi',        'Shini Yasui Kōshaku Reijō to Shichi-nin no Kikōshi',                     'translated'),
		('Stepbrother\'s Diary',                                      'Lean Tuna and Her Stepbrother’s Plan to Become a Fatty Tuna',            'translated'),
		('MaguToro',                                                  'Lean Tuna and Her Stepbrother’s Plan to Become a Fatty Tuna',            'translated'),
		('Lewd Game',                                                 'I Decided to Participate in a Lewd Game in My Dream',                    'translated'),
		('summoned hero',                                             'I Summoned the Hero, to the Present Age',                                'translated'),
		('Seven Nobles',                                              'Duke\'s Daughter who is Liable to Die and the Seven Nobles',             'translated'),
		('Erica',                                                     'Duke\'s Daughter who is Liable to Die and the Seven Nobles',             'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	chp_prefixes = [
			('IDWBV – ',  'I Don’t Want to Become a Villainess, So I Aim at Becoming a Perfect Lady Together with the Prince!',               'translated'), 
		]

	for prefix, series, tl_type in chp_prefixes:
		if item['title'].lower().startswith(prefix.lower()):
			return buildReleaseMessageWithType(item, series, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



	return False