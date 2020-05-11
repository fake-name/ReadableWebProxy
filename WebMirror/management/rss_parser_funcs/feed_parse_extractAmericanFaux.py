def extractAmericanFaux(item):
	"""
	Parser for 'American Faux'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
		
	tagmap = [
		('Yuusha Ni Narenakatta Ore Wa Isekai De',                                                                 'Yuusha ni Nare Nakatta Ore wa Shibushibu Shuushoku o Ketsui Shimashita',                                                  'translated'),
		('Isekai Mahou Isekai Mahou ha Okureteru!',                                                                'Isekai Mahou Isekai Mahou ha Okureteru!',                                                                                 'translated'),
		('Yankee wa Isekai de Seirei ni Aisaremasu.',                                                              'Yankee wa Isekai de Seirei ni Aisaremasu.',                                                                               'translated'),
		('The Day I Disappeared',                                                                                  'The Day I Disappeared',                                                                                                   'translated'),
		('The Heir of the Dragon Emperor and his Bride Corps',                                                     'The Heir of the Dragon Emperor and his Bride Corps',                                                                      'translated'),
		('The Witch Who Once Was Called A Saint',                                                                  'The Witch Who Once Was Called A Saint',                                                                                   'translated'),
		('A Thousand Years of Separation~ Today, I Shall be the Villainess~',                                      'A Thousand Years of Separation~ Today, I Shall be the Villainess~',                                                       'translated'),
		('Kenshin no Keishousha',                                                                                  'Kenshin no Keishousha',                                                                                                   'translated'),
		('I, a Witch, am Requested by My Crush to Make Him Love Potion',                                           'I, a Witch, am Requested by My Crush to Make Him Love Potion',                                                            'translated'),
		('We Dwell at the Base of the Dragon’s Peak',                                                              'We Dwell at the Base of the Dragon’s Peak',                                                                               'translated'),
		('Only I can Return After the Class Transfer',                                                             'Only I can Return After the Class Transfer',                                                                              'translated'),
		('Sore, Itadakimasu',                                                                                      'Sore, Itadakimasu',                                                                                                       'translated'),
		('Isekai Mahou ha Okureteru!',                                                                             'Isekai Mahou ha Okureteru!',                                                                                              'translated'),
		('Saikyou Mahoushi no Inton Keikaku',                                                                      'Saikyou Mahoushi no Inton Keikaku',                                                                                       'translated'),
		('the noble girl who finds a nerdy and plain guy moe thinks that the arrogant prince is in the way',       'the noble girl who finds a nerdy and plain guy moe thinks that the arrogant prince is in the way',                        'translated'),
		('the returnee noble lady attacks his majesty the dragon emperor',                                         'the returnee noble lady attacks his majesty the dragon emperor',                                                          'translated'),
		('i don\'t want to break off my engagement...',                                                            'i don\'t want to break off my engagement...',                                                                             'translated'),
		('the kingdom of everlasting night and the last ball',                                                     'the kingdom of everlasting night and the last ball',                                                                      'translated'),
		('your highness, the voice of your heart is leaking!',                                                     'your highness, the voice of your heart is leaking!',                                                                      'translated'),
		('i am a duchess who has rewound nine times, but my tenth life seems to be a reward mode',                 'i am a duchess who has rewound nine times, but my tenth life seems to be a reward mode',                                  'translated'),
		('formerly a fallen duke\'s daughter',                                                                     'formerly a fallen duke\'s daughter',                                                                                      'translated'),
		('.hack//C.S.',                                                                                            '.hack//C.S.',                                                                                                             'translated'),
		('The Wandering World',                                                'The Wandering World',                                                                 'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False