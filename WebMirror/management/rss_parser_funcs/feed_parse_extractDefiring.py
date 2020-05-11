def extractDefiring(item):
	"""
	# Defiring

	"""

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

		
	tagmap = [
		('Almadinos Eiyuuden',                        'Almadinos Eiyuuden',                       'translated'),
		('Tsuyokute New Saga',                        'Tsuyokute New Saga (LN)',                  'translated'),
		('population control',                        'population control',                       'translated'),
		('the demon lord is suing the hero',          'Maou Dakedo Yuushano Koto Kokuso Suru Kotoni Shitakara',                            'translated'),
		('World teacher',                             'World teacher',                            'translated'),
		('My Death Flags Show No Sign of Ending',     'My Death Flags Show No Sign of Ending',    'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	if item['tags'] == ['Non classé']:
		titlemap = [
			('World teacher',                                       'World teacher',                            'translated'),
			('Shinka no Mi',                                        'Shinka no Mi',                             'translated'),
			('My death Flags show no Sign of Ending – Chapter',     'My Death Flags Show No Sign of Ending',    'translated'),
			('Almadianos Eiyuuden',                                 'Almadinos Eiyuuden',                       'translated'),
			('Almadinos Eiyuuden',                                  'Almadinos Eiyuuden',                       'translated'),
		]

		for titlecomponent, name, tl_type in titlemap:
			if titlecomponent.lower() in item['title'].lower():
				return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
	return False