def extractExiledrebelsscanlationsCom(item):
	'''
	Parser for 'exiledrebelsscanlations.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	if 'Manga' in item['tags']:
		return None

	tagmap = [
		("i’m using the interstellar live broadcast to raise cubs",     "i’m using the interstellar live broadcast to raise cubs",          'translated'),
		("President isn’t ‘Mary Sue’",                                  "President isn’t 'Mary Sue'",                                       'translated'),
		('I am a Chef in the Modern Era',                               'I am a Chef in the Modern Era',                                    'translated'),
		('If Only Time Stopped at the Moment We First Met',             'If Only Time Stopped at the Moment We First Met',                  'translated'),
		('My Wife Always Thought I Did Not Love Him (Rebirth)',         'My Wife Always Thought I Did Not Love Him (Rebirth)',              'translated'),
		('The Palaces of the Twelve Sacred Beasts',                     'The Palaces of the Twelve Sacred Beasts',                          'translated'),
		('Gaze at the Scenes of Debauchery',                            'Gaze at the Scenes of Debauchery',                                 'translated'),
		('Spring Trees and Sunset Clouds',                              'Spring Trees and Sunset Clouds',                                   'translated'),
		('Grandmaster of Demonic Cultivation',                          'Grandmaster of Demonic Cultivation',                               'translated'),
		('LMW Chapters',                                                'The Legendary Master\'s Wife',                                     'translated'),
		('The Legendary Master\'s Wife',                                'The Legendary Master\'s Wife',                                     'translated'),
		('i heard that my fiance is super fierce',                      'i heard that my fiance is super fierce',                           'translated'),
		('Sickly Tyrannical',                                           'Sickly Tyrannical',                                                'translated'),
		('forced estrus [abo]',                                         'forced estrus [abo]',                                              'translated'),
		('ageless seducer',                                             'ageless seducer',                                                  'translated'),
		('A Heart of a Smith',                                          'A Heart of a Smith',                                               'translated'),
		('beast store no. 138',                                         'Cute Beast Store No. 138',                                         'translated'),
		('delicious food got me famous across the galaxy',              'delicious food got me famous across the galaxy',                   'translated'),
		('retirement life (ancient transmigration)',                    'Retirement Life (Ancient Transmigration)',                         'translated'),
		('Mr. Fashionable',                                             'Mr. Fashionable',                                                  'translated'),
		('Lessons on Raising a Partner',                                'Lessons on Raising a Partner',                                     'translated'),
		('quick transmigration: lovers always on the counterattack',    'quick transmigration: lovers always on the counterattack',         'translated'),
		('hnmsghml chapters',                                           'he\'s not my shadow guard, he\'s my lover',                        'translated'),
		('he\'s not my shadow guard, he\'s my lover',                   'he\'s not my shadow guard, he\'s my lover',                        'translated'),
		('Spirit Hotel',                                                'Spirit Hotel',                                                     'translated'),
		('Never, My Alpha',                                             'Never, My Alpha',                                                  'oel'), 
		('Fractured Moonlight',                                         'Fractured Moonlight',                                              'oel'), 
		('Inked',                                                       'Inked',                                                            'oel'), 
		('Only Mine Chapters',                                          'Only Mine',                                                        'oel'), 
		('OM Chapters',                                                 'Only Mine',                                                        'oel'), 
		('Secrets Within the Resounding Sound',                         'Secrets Within the Resounding Sound',                              'oel'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



	return False