def extractTheLazy9(item):
	"""
	# TheLazy9
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
		
	tagmap = [
		('HTG',                                                                'I was Reincarnated as a Thief Girl and my Mission is to Harass the Demon Lord and the Hero.',      'translated'),
		('Just Loving You',                                                    'Just Loving You',                                                                                  'translated'),
		('かんすとっぷ！(KANSUTOPPU)',                                         'Kansutoppu!',                                                                                      'translated'),
		('Goblin Tenseiki ~erufu youjo ni kaku de maketeru yuusha na ore~',    'Goblin Tenseiki ~erufu youjo ni kaku de maketeru yuusha na ore~',                                  'translated'),
		('Job Change',                                                         'Being Recognized as an Evil God, I Changed My Job to Guardian Deity of the Beastmen Country',      'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
	titlemap = [
		('Tridente',                                   'Small Village Tridente',                                                                           'translated'),
		('Just Loving You',                            'Just Loving You',                                                                                  'translated'),
		('Black Knight',                               'The Black Knight Who Was Stronger than even the Hero',                                             'translated'),
		('Astarte’s Knight',                           "Astarte's Knight",                                                                                 'translated'),
		('HTG:',                                       'Tozoku shoujo ni tensei shita ore no shimei wa yuusha to maou ni iyagarasena no!',                 'translated'),
		('Kansutoppu!',                                'Kansutoppu!',                                                                                      'translated'),
		('The Lonely Monster and The Blind Girl ',     'The Lonely Monster and The Blind Girl',                                                            'translated'),
		('Job Change',                                 'Being Recognized as an Evil God, I Changed My Job to Guardian Deity of the Beastmen Country',      'translated'),
		('Orgegirl ch',                                'Blunt Type Ogre Girl’s Way to Live Streaming',                                                     'translated'),
		('Ogregirl ch',                                'Blunt Type Ogre Girl’s Way to Live Streaming',                                                     'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
	chp_prefixes = [
			('Manowa',  'Manowa Mamono Taosu Nouryoku Ubau Watashi Tsuyokunaru',               'translated'),
			('Cat ',    'Me and My Beloved Cat (Girlfriend)',                                  'translated'),
			('Kansu ',  'Kansutoppu!',                                                         'translated'),
			('YMC ',    'Yuri Maid Cafe',                                                      'translated'),
			('Gob ',    'Goblin Tenseiki ~erufu youjo ni kaku de maketeru yuusha na ore~',     'translated'),
		]

	for prefix, series, tl_type in chp_prefixes:
		if item['title'].lower().startswith(prefix.lower()):
			return buildReleaseMessageWithType(item, series, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
	return False