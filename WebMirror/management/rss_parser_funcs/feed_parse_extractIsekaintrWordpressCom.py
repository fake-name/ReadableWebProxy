def extractIsekaintrWordpressCom(item):
	'''
	Parser for 'isekaintr.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Saint Doll',                                                                              'Seikishin -Saint Doll-',                                                              'translated'),
		('When I was summoned to different world with RPG style, [Loves NTR] skill appeared',       'When I was summoned to different world with RPG style, [Likes NTR] skill appeared',   'translated'),
		('When I was summoned to different world with RPG style, [Likes NTR] skill appeared',       'When I was summoned to different world with RPG style, [Likes NTR] skill appeared',   'translated'),
		('When I was summoned to another world with RPG style, [Likes NTR] skill appeared',         'When I was summoned to different world with RPG style, [Likes NTR] skill appeared',   'translated'),
		('Loiterous',                                                                               'Loiterous',                                                                           'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



	return False