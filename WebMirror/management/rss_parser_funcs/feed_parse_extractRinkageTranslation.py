def extractRinkageTranslation(item):
	"""
	'Rinkage Translation'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None

	tagmap = [


		('Netooku Otoko no Tanoshii Isekai Boueki',  'Netooku Otoko no Tanoshii Isekai Boueki',                        'translated'),
		('Atelier Tanaka',                           'Atelier Tanaka',                                                 'translated'),
		('Din No Monshou',                           'Din No Monshou',                                                 'translated'),
		('Sonohi Sekai ga Kawatta',                  'Sonohi Sekai ga Kawatta',                                        'translated'),
		('Yuusha Party (WN)',                        'Yuusha Party no Kawaii Ko ga Ita no de, Kokuhaku Shite (WN)',    'translated'),
		('Yuusha Party (LN)',                        'Yuusha Party no Kawaii Ko ga Ita no de, Kokuhaku Shite (LN)',    'translated'),
		('Netooku Otoko (LN)',                       'Netooku Otoko no Tanoshii Isekai Boueki (LN)',                   'translated'),
		('Netooku Otoko (WN)',                       'Netooku Otoko no Tanoshii Isekai Boueki (WN)',                   'translated'),
		('Netooku Otoko',                            'Netooku Otoko no Tanoshii Isekai Boueki',                        'translated'),
		('Yuusha Party',                             'Yuusha Party ni Kawaii Ko ga Ita node, Kokuhaku Shitemita.',     'translated'),
		('Netooku Otoko',                            'Netooku Otoko no Tanoshii Isekai Boueki',                        'translated'),
		('Sonohi Sekai ga Kawatta',                  'Sonohi Sekai ga Kawatta',                                        'translated'),
		('Din No Monshou',                           'Din No Monshou',                                                 'translated'),
		('My Beautiful Teacher',                     'My Beautiful Teacher',                                           'translated'),
		('Yuusha Party',                             'Yuusha Party',                                                   'translated'),
		('Yuusha Party (LN)',                        'Yuusha Party no Kawaii Ko ga Ita no de, Kokuhaku Shite (LN)',    'translated'),
	]                

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	return False