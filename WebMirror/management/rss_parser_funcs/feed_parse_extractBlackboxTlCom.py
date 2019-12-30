def extractBlackboxTlCom(item):
	'''
	Parser for 'blackbox-tl.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('The Antelope and Night Wolf',                   'The Antelope and Night Wolf',                                  'translated'),
		('awm',                                           'AWM: PUBG',                                                    'translated'),
		('LRotPB',                                        'Lantern: Reflection of the Peach Blossoms',                    'translated'),
		('SASAM',                                         'My Senior Is Always Salivating After Me',                      'translated'),
		('My Senior Is Always Salivating After Me',       'My Senior Is Always Salivating After Me',                      'translated'),
		('TSNLT',                                         'The Script Is Not Like This',                                  'translated'),
		('The Script Is Not Like This',                   'The Script Is Not Like This',                                  'translated'),
		('ISMM',                                          'I Ship My Adversary X Me',                                     'translated'),
		('I Ship My Adversary X Me',                      'I Ship My Adversary X Me',                                     'translated'),
		('QZ',                                            'Qizi',                                                         'translated'),
		('Qizi',                                          'Qizi',                                                         'translated'),
		('Ta',                                            'Thousand Autumns',                                             'translated'),
		('Thousand Autumns',                              'Thousand Autumns',                                             'translated'),
		('TYQHM',                                         'Those Years In Quest of Honour Mine',                          'translated'),
		('POBE',                                          'A President\'s Out-of-Body Experience',                        'translated'),
		('A President\'s Out-of-Body Experience',         'A President\'s Out-of-Body Experience',                        'translated'),
		('Peerless',                                      'Peerless',                                                     'translated'),
		('Slow-Witted',                                   'Slow-Witted',                                                  'translated'),
		('Breaking through the Clouds',                   'Breaking through the Clouds',                                  'translated'),
		('HoG',                                           'Heart of Glass',                                               'translated'),
		('heart of glass',                                'Heart of Glass',                                               'translated'),
		('Fuck Off Unless You\'re The One',               'Fuck Off Unless You\'re The One',                              'translated'),
		('FOYO',                                          'Fuck Off Unless You\'re The One',                              'translated'),
		('A Fox Spirit\'s Guide to Sleeping with Men',    'A Fox Spirit\'s Guide to Sleeping with Men',                   'translated'),
		('FSGSM',                                         'A Fox Spirit\'s Guide to Sleeping with Men',                   'translated'),
		('YGMCT',                                         'You\'ve Got Mail: A Cautionary Tale',                          'translated'),
		('You\'ve Got Mail: A Cautionary Tale',           'You\'ve Got Mail: A Cautionary Tale',                          'translated'),
		('A Race to (Be) The Top',                        'A Race to (Be) The Top',                                       'translated'),
		('Muted',                                         'Muted',                                                        'translated'),
		('MLP',                                           'My Little Poplar',                                             'translated'),
		('My Little Poplar',                              'My Little Poplar',                                             'translated'),
		('Times of Our Lives',                            'Times of Our Lives',                                           'translated'),
		('CFSB',                                          '[Rebirth] The Cannon Fodder Strikes Back',                     'translated'),
		('[Rebirth] The Cannon Fodder Strikes Back',      '[Rebirth] The Cannon Fodder Strikes Back',                     'translated'),
		('creatures of habit',                            'Creatures of Habit',                                           'translated'),
		('Winner Takes All',                              'Winner Takes All',                                             'translated'),
		('Undead',                                        'Undead',                                                       'translated'),
		('Love Expired',                                  'Love Expired',                                                 'translated'),
		('how to survive as a villain',                   'how to survive as a villain',                                  'translated'),
		('chasing tides',                                 'chasing tides',                                                'translated'),
		('the elegant dancing years',                     'the elegant dancing years',                                    'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False