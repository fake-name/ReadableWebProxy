def extractWwwLightnovelsonlineNet(item):
	'''
	Parser for 'www.lightnovelsonline.net'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('The Defeated Dragon',                                                                       'The Defeated Dragon',                                                                                      'translated'),
		('Mechanical God Emperor',                                                                    'Mechanical God Emperor',                                                                                   'translated'),
		('The Record of My Sex Life in a Different World',                                            'The Record of My Sex Life in a Different World',                                                           'translated'),
		('Serena- The Futanari Princess',                                                             'Serena - The Futanari Princess',                                                                           'translated'),
		('Junior High School Sex Slave Runa',                                                         'Junior High School Sex Slave Runa',                                                                        'translated'),
		('A World Where All Women Are Managed By Men',                                                'A World Where All Women Are Managed By Men',                                                               'translated'),
		('Api di Bukit Menoreh',                                                                      'Fire in the Menoreh Mountain',                                                                             'translated'),
		('Hypnotized Harem',                                                                          'Hypnotized Harem',                                                                                         'translated'),
		('Prisoner\'s love: The Devil\'s mark',                                                       'Prisoner\'s love: The Devil\'s mark',                                                                      'translated'),
		('Beautiful Females in the Underground Prison',                                               'Beautiful Females in the Underground Prison',                                                              'translated'),
		('I Have The Only Ero Knowledge In The World, So I Decided To Cum Inside Pretty Girls',       'I Have The Only Ero Knowledge In The World, So I Decided To Cum Inside Pretty Girls',                      'translated'),
		('World Class Prostitution ring',                                                             'World Class Prostitution ring',                                                                            'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False