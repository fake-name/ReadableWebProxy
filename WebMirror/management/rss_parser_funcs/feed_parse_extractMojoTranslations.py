def extractMojoTranslations(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Synopsis - Summaries' in item['tags']:
		return None
	# Apparently manga?
	if 'Air Master' in item['tags']:
		return None
		
	tagmap = [
		('Duke\'s Daughter and Knight Captain(62)',               'The Duke\'s Daughter Is the Knight Captain\'s (62) Young Wife',                'translated'), 
		('Drop!!',                                                'Drop!! ~A Tale of the Fragrance Princess~',                                    'translated'), 
		('Heibon na Watashi wa Tonikaku Hibon',                   'Heibon na Watashi wa Tonikaku Hibon',                                          'translated'), 
		('Around 30',                                             'I am the Newly Born Woman of Around Thirty',                                   'translated'), 
		('The corner is fine. Please don\'t mind me',             'The corner is fine. Please don\'t mind me',                                    'translated'), 
		('Isekai de Mofumofu Nadenade Suru Tame ni Ganbattemasu', 'Isekai de Mofumofu Nadenade Suru Tame ni Ganbattemasu',                        'translated'), 
		('Isekai de Mofumofu Nadenade no Tame ni Ganbattemasu',   'Isekai de Mofumofu Nadenade Suru Tame ni Ganbattemasu',                        'translated'), 
		('Yankee wa Isekai de Seirei ni Aisaremasu',              'Yankee wa Isekai de Seirei ni Aisaremasu',                                     'translated'), 
		('Akuyaku Reijou wa Danna-sama wo Yasesasetai',           'Akuyaku Reijou wa Danna-sama wo Yasesasetai',                                  'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False