def extractCclawtranslationsHomeBlog(item):
	'''
	Parser for 'cclawtranslations.home.blog'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	if item['tags'] == ['Allgemein']:
		titlemap = [
			('Ore Ga Suki Nano Wa Imouto Dakedo Imouto Janai',                  'Ore Ga Suki Nano Wa Imouto Dakedo Imouto Janai',                                                        'translated'),
			('Kawaikereba Hentai demo Suki ni Natte Kuremasu Ka? Volume',       'Kawaikereba Hentai demo Suki ni Natte Kuremasu Ka?',                                                    'translated'),
			('Boku no Kanojo Sensei Volume ',                                   'Boku no Kanojo Sensei',                                                                                 'translated'),
			('Berserk of Gluttony (LN) Volume ',                                'Berserk of Gluttony (LN)',                                                                              'translated'),
			('Tomodachi no Imouto ga Ore ni Dake Uzai Volume ',                 'Tomodachi no Imouto ga Ore ni Dake Uzai',                                                               'translated'),
			('Naze Boku no Sekai wo Daremo Oboeteinai no ka? Volume ',          'Naze Boku no Sekai wo Daremo Oboeteinai no ka?',                                                        'translated'),
			('Jishou F-Rank no Oniisama ',                                      'Jishou F-Rank no Oniisama ga Game de Hyouka sareru Gakuen no Chouten ni Kunrin suru Sou desu yo?',      'translated'),
			('Osananajimi ga Zettai ni Makenai Love Comedy Volume ',            'Osananajimi ga Zettai ni Makenai Love Comedy',                                                          'translated'),
			('Kawaii Onnanoko ni Kouryaku Sareru no Wa Suki desu ka? Volume ',  'Kawaii Onnanoko ni Kouryaku Sareru no Wa Suki desu ka?',                                                'translated'),
			('Tensei Shoujo no Rirekisho',  'Tensei Shoujo no Rirekisho',      'translated'),
			('Master of Dungeon',           'Master of Dungeon',               'oel'),
		]

		for titlecomponent, name, tl_type in titlemap:
			if titlecomponent.lower() in item['title'].lower():
				return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False