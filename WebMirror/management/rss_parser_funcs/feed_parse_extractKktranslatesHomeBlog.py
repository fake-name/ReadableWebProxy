def extractKktranslatesHomeBlog(item):
	'''
	Parser for 'kktranslates.home.blog'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Go to Hell. White Lotus',                             'Go to Hell. White Lotus',                                            'translated'),
		('My Wife is Straight',                                 'My Wife is Straight',                                                'translated'),
		('My Enemy is Actually Secretly in Love with Me',       'My Enemy is Actually Secretly in Love with Me',                      'translated'),
		('Love Rival Romance System',                           'Love Rival Romance System',                                          'translated'),
		('The Cutest Height Difference',                        'The Cutest Height Difference',                                       'translated'),
		('i rely on kisses to clear survival games',            'i rely on kisses to clear survival games',                           'translated'),
		('to be a heartthrob in a horror movie',                'to be a heartthrob in a horror movie',                               'translated'),
		('global university entrance examination',              'global university entrance examination',                             'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False