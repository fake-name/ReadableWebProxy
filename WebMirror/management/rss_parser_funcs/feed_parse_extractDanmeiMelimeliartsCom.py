def extractDanmeiMelimeliartsCom(item):
	'''
	Parser for 'danmei.melimeliarts.com'
	'''
	
	
	badwords = [
			'[Audio Drama]',
		]
	tstr = str(item['tags'])
	if any([bad in tstr for bad in badwords]):
		return None



	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('parenting in full bloom! the former villainous noble son who found his love nest',       'parenting in full bloom! the former villainous noble son who found his love nest',                      'translated'),
		('As the Minor Gay Love Rival in Het Novels',    'As the Minor Gay Love Rival in Het Novels',                                                                  'translated'),
		('Strategy to Capture That Scum Gong',           'Strategy to Capture That Scum Gong',                                                                         'translated'),
		('SCSG',                                         'Strategy to Capture That Scum Gong',                                                                         'translated'),
		('Fantasy Farm',                                 'Fantasy Farm',                                                                                               'translated'),
		('Vanguard of the Eternal Night',                'Vanguard of the Eternal Night',                                                                              'translated'),
		('Don\'t You Like Me',                           'Don\'t You Like Me',                                                                                         'translated'),
		('Lord of End of World',                         'Lord of End of World',                                                                                       'translated'),
		('Who Touched My Tail!',                         'Who Touched My Tail!',                                                                                       'translated'),
		('Raising a Bun with a Daily Life System',       'Raising a Bun with a Daily Life System',                                                                     'translated'),
		('Perfect Destiny',                              'Quick Transmigration: Perfect Destiny Summary',                                                              'translated'),
		('Rebirth of the Supreme Celestial Being',       'Rebirth of the Supreme Celestial Being',                                                                     'translated'),
		('There Will Always Be Protagonists With Delusions of Starting a Harem',   'There Will Always Be Protagonists With Delusions of Starting a Harem',             'translated'),
		('My Cherry Will Explode in the Apocalypse',                               'My Cherry Will Explode in the Apocalypse',                                         'translated'),
		('It’s Actually Not Easy Wanting to be a Supporting Male Lead',            'It’s Actually Not Easy Wanting to be a Supporting Male Lead',                      'translated'),
		('Seizing Dreams',                                                         'Seizing Dreams',                                                                   'translated'),
		('Back to the Apocalypse',                                                 'Back to the Apocalypse',                                                           'translated'),
		('Killing The Same Person Every Time',                                     'Killing The Same Person Every Time',                                               'translated'),
		('Don\'t Pick Up Boyfriends From the Trash Bin',                           'Don\'t Pick Up Boyfriends From the Trash Bin',                                     'translated'),
		('Game, Live Broadcast',                                                   'Game, Live Broadcast',                                                             'translated'),
		('First Lazy Merchant of the Beast World',                                 'Number One Lazy Merchant of the Beast World',                                      'translated'),
		('Number One Lazy Merchant of the Beast World',                            'Number One Lazy Merchant of the Beast World',                                      'translated'),
		('Game, Live Stream',                                                      'Game, Live Stream',                                                                'translated'),
		('This World Has Gone Crazy',                                              'This World Has Gone Crazy',                                                        'translated'),
		('My Vegetative Partner Opened His Eyes in Anger After I Ran Away',        'My Vegetative Partner Opened His Eyes in Anger After I Ran Away',                  'translated'),
		('The Demon King Always Thinks I\'m Secretly in Love with Him',            'The Demon King Always Thinks I\'m Secretly in Love with Him',                      'translated'),
		('Nurturing the Hero to Avoid Death',                                      'Nurturing the Hero to Avoid Death',                                                'translated'),
		('Ever Since I Take Home An Adonis Who Has Lost His Business',             'Ever Since I Take Home An Adonis Who Has Lost His Business',                       'translated'),
		('Stone Age Husband Raising Journal',                                      'Stone Age Husband Raising Journal',                                                'translated'),
		('quickly wear the face of the devil (extra 2)',                           'Quickly Wear the Face of the Devil',                                               'translated'),
		('Quickly Wear the Face of the Devil (Extra 4)',                           'Quickly Wear the Face of the Devil',                                               'translated'),
		('Peach Blossom Debt',                                                     'Peach Blossom Debt',                                                               'translated'),
		('Shh, There\'s a Beast in the Imperial Palace',                           'Shh, There\'s a Beast in the Imperial Palace',                                     'translated'),
		('The #1 Pretty Boy of the Immortal Path',                                 'The #1 Pretty Boy of the Immortal Path',                                           'translated'),
		('Dinghai Fusheng Records',                                                'Dinghai Fusheng Records',                                                          'translated'),
		('Strong Offense and Defense',                                             'Strong Offense and Defense',                                                       'translated'),
		('the villain’s face-slapping counterattack',                              'The Villain\'s Face Slapping Counterattack',                                       'translated'),
		('marshal, please calm down',                                              'Marshal, Please Calm Down',                                                        'translated'),
		('i have medicine',                                                        'i have medicine',                                                                  'translated'),
		('new times, new hell',                                                    'new times, new hell',                                                              'translated'),
		('the king\'s game',                                                       'the king\'s game',                                                                 'translated'),
		('itâ€™s actually not easy wanting to be a supporting male lead',          'it\'s actually not easy wanting to be a supporting male lead',                     'translated'),
		('yin yang eye gungunâ€™s marriage contract',                              'yin yang eye gungun\'s marriage contract',                                        'translated'),
		('the film emperor\'s daily live cooking broadcast',                       'the film emperor\'s daily live cooking broadcast',                                 'translated'),
		('boss\'s guide to seeking death',                                         'boss\'s guide to seeking death',                                                   'translated'),
		('the general loves to collect little red flowers',                        'the general loves to collect little red flowers',                                  'translated'),
		('it\'s easy to take care of a live-in hero!',                             'it\'s easy to take care of a live-in hero!',                                       'translated'),
		('i\'m not human',                                                         'i\'m not human',                                                                   'translated'),
		('card room (rebirth)',                                                    'card room (rebirth)',                                                              'translated'),
		('guide on how to fail at online dating',                                  'guide on how to fail at online dating',                                            'translated'),
		('Fei Pin Ying Qiang',                                                     'Fei Pin Ying Qiang',                                                               'translated'),
		('loneliness',                                                             'loneliness',                                                                       'translated'),
		('surprise! the supposed talent show was actuallyâ€“?!',                   'Surprise! The Supposed Talent Show Was Actually–?!',                               'translated'),
		('surprise! the supposed talent show was actually–?!',                     'Surprise! The Supposed Talent Show Was Actually–?!',                               'translated'),
		('if you don\'t fall in love, you\'ll die',                                'If You Don\'t Fall In Love, You\'ll Die',                                          'translated'),
		('yin yang eye gungun’s marriage contract',                                'yin yang eye gungun’s marriage contract',                                          'translated'),
		('The Wife is First',                                                      'The Wife is First',                                                                'translated'),
		('i wasn\'t born lucky',                                                   'i wasn\'t born lucky',                                                             'translated'),
		('reborn with an old enemy on the day of our marriage',                    'reborn with an old enemy on the day of our marriage',                              'translated'),
		('Befriending The Most Powerful Person',                                   'Befriending The Most Powerful Person',                                             'translated'),
		('class teacher system',                                                   'class teacher system',                                                                  'translated'),
		('Stop Bothering Me, Emperor',                                             'Stop Bothering Me, Emperor',                                                            'translated'),
		('what should i do if the school bully is interested in me',               'what should i do if the school bully is interested in me',                              'translated'),
		('the white cat\'s divine scratching post',                                'the white cat\'s divine scratching post',                                               'translated'),
		('desharow merman',                                                        'desharow merman',                                                                       'translated'),
		('holding onto my man',                                                    'holding onto my man',                                                                   'translated'),
		('later, he became a royal healer',                                        'later, he became a royal healer',                                                       'translated'),
		('tattoo',                                                                 'tattoo',                                                                                'translated'),
		('blooming romance',                                                       'blooming romance',                                                                      'translated'),
		('very happy',                                                             'very happy',                                                                            'translated'),
		('the a in the opposite dorm always thinks i\'m pretending to be a b',     'the a in the opposite dorm always thinks i\'m pretending to be a b',                    'translated'),
		('fake dating the amnesiac school prince',                                 'fake dating the amnesiac school prince',                                                'translated'),
		('the seeing eye dog',                                                     'the seeing eye dog',                                                                    'translated'),
		('quick transmigration: i\'m almost dead',                                 'quick transmigration: i\'m almost dead',                                                'translated'),
		('reborn into a slash game',                                               'reborn into a slash game',                                                              'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False