def extractWwwDreampotatoCom(item):
	'''
	Parser for 'www.dreampotato.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Magi’s Grandson',                                              'Magi\'s Grandson',                                                            'translated'),
		('I Was a Sword When I Reincarnated (WN)',                       'I Was a Sword When I Reincarnated (WN)',                                      'translated'),
		('Tensei Saki ga Shoujo Manga no Shiro Buta Reijou datta',       'Tensei Saki ga Shoujo Manga no Shiro Buta Reijou datta',                      'translated'),
		('Otoko Nara Ikkokuichijou no Aruji o Mezasa Nakya, ne?',        'Otoko Nara Ikkokuichijou no Aruji o Mezasa Nakya, ne?',                       'translated'),
		('The Lazy Swordmaster',                                         'The Lazy Swordmaster',                                                        'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False