def extractEroLightNovelTranslations(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
		
	if 'Adolescent Adam' in item['tags']:
		if 'Adolescent Adam 2' in item['title']:
			if not vol:
				vol = 1
			return buildReleaseMessageWithType(item, 'Shishunki na Adam', vol + 1, chp, frag=frag, postfix=postfix)
		return buildReleaseMessageWithType(item, 'Shishunki na Adam', vol, chp, frag=frag, postfix=postfix)


	tagmap = [
		('Makina',                                             'The Slutty Adventures of Magical Princess Makina',                    'translated'),
		('Harem Castle',                                       'Harem Castle',                                                        'translated'),
		('Harem Pirates',                                      'Harem Pirates',                                                       'translated'),
		("Student Council President's Secret Laid Bare",       "Student Council President's Secret Laid Bare",                        'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)
			
	chp_prefixes = [
			('Milk Princess',                                        'Milk Princess',                                            'translated'),
			('Harem Dynast',                                         'Harem Dynast',                                             'translated'),
			('Harem Engagement',                                     'Harem Engagement',                                         'translated'),
			('Harem Sister',                                         'Harem Sister',                                             'translated'),
			('Harem Caravan',                                        'Harem Caravan',                                            'translated'),
			('Erogenous Beauty Salon by Succubus Girls: Chapter',    'Erogenous Beauty Salon by Succubus Girls',                 'translated'),
			('Erogenous Beauty Salon by Succubus Girls 2: Chapter',  'Erogenous Beauty Salon by Succubus Girls 2',               'translated'),
		]

	for prefix, series, tl_type in chp_prefixes:
		if item['title'].lower().startswith(prefix.lower()):
			return buildReleaseMessageWithType(item, series, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


			

	return False