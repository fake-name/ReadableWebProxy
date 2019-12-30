def extractHornytranslationsWordpressCom(item):
	'''
	Parser for 'hornytranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Junior High School Sex Slave Runa',                                                     'Junior High School Sex Slave Runa',                                                    'translated'),
		('Women\'s Dormitory Manager',                                                            'Women\'s Dormitory Manager',                                                           'translated'),
		('Valhalla - The Penis Mansion',                                                          'Valhalla - The Penis Mansion',                                                         'translated'),
		('The Day My Sister Became an Exclusive Meat Toilet',                                     'The Day My Sister Became an Exclusive Meat Toilet',                                    'translated'),
		('I Have The Only Ero Knowledge In The World, So I Decided To Cum Inside Pretty Girls',   'I Have The Only Ero Knowledge In The World, So I Decided To Cum Inside Pretty Girls',  'translated'),
		('The Record of My Sex Life in a Different World',                                        'The Record of My Sex Life in a Different World',                                       'translated'),
		('My Elder Sister Fell in Love with Me and Transformed into a Yandere',                   'My Elder Sister Fell in Love with Me and Transformed into a Yandere',                  'translated'),
		('Chronicles of a Creative Different World Reincarnation',                                'Chronicles of a Creative Different World Reincarnation',                               'translated'),
		('The Duo Who Hunt Women',                                                                'The Duo Who Hunt Women',                                                               'translated'),
		('Fate Comes with Time',                                                                  'Fate Comes with Time',                                                                 'translated'),
		('World Class Prostitution ring',                                                         'World Class Prostitution ring',                                                        'translated'),
		('Serena – The Futanari Princess',                                                        'Serena – The Futanari Princess',                                                       'translated'),
		('Princess Insult',                                                                       'Princess Insult',                                                                      'translated'),
		('Marriage Insult',                                                                       'Marriage Insult',                                                                      'translated'),
		('Hypnotized Harem',                                                                      'Hypnotized Harem',                                                                     'translated'),
		('International Sex Slave Law',                                                           'International Sex Slave Law',                                                          'translated'),
		('Books to Dominate Married Women',                                                       'Books to Dominate Married Women',                                                      'translated'),
		('Beautiful Females in the Underground Prison',                                           'Beautiful Females in the Underground Prison',                                          'translated'),
		('A World Where All Women Are Managed By Men',                                            'A World Where All Women Are Managed By Men',                                           'translated'),
		('The Training Record of a Married Woman',                                                'The Training Record of a Married Woman',                                               'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False