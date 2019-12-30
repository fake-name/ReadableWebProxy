def extractInfiniteNovelTranslations(item):
	"""
	# Infinite Novel Translations

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None

	tagmap = [
		('Ascendance of a Bookworm',                                   'Ascendance of a Bookworm',                              'translated'), 
		('Yomigaeri no Maou',                                          'Yomigaeri no Maou',                                     'translated'), 
		('Kakei Senki wo Kakageyo!',                                   'Kakei Senki wo Kakageyo!',                              'translated'), 
		('Kuro no Shoukan Samurai',                                    'Kuro no Shoukan Samurai',                               'translated'), 
		('Nidoume no Jinsei wo Isekai de',                             'Nidoume no Jinsei wo Isekai de',                        'translated'), 
		('Hachi-nan',                                                  'Hachinan tte, Sore wa Nai Deshou!',                     'translated'), 
		('Summoned Slaughterer',                                       'Yobidasareta Satsuriku-sha',                            'translated'), 
		('maou no utsuwa',                                             'Maou no Utsuwa',                                        'translated'), 
		('Maou no Ki',                                                 'Maou no Ki',                                            'translated'), 
		('Imperial wars and my stratagems',                            'Imperial Wars and my Stratagems',                       'translated'), 
		('Kuro no Shoukanshi',                                         'Kuro no Shoukanshi',                                    'translated'), 
		('I work as Healer in Another World\'s Labyrinth City',        'I work as Healer in Another World\'s Labyrinth City',   'translated'), 
		('The Spearmaster and The Black Cat',                          'The Spearmaster and The Black Cat',                     'translated'), 
		('Hakai no Miko',                                              'Hakai no Miko',                                         'translated'),
		
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
	return False