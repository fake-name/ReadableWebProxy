def extractWwwSigmanovelCom(item):
	'''
	Parser for 'www.sigmanovel.com'
	'''
	if 'Teasers' in item['tags']:
		return None
		
		
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Martial God Conquerer',          'Martial God Conquerer',                         'translated'),
		('World Controlling God',          'World Controlling God',                         'translated'),
		('Above The Skies',                'Above The Skies',                               'translated'),
		('Sage Emperor',                   'Sage Emperor',                                  'translated'),
		('The Mysterious Apartment',       'The Mysterious Apartment',                      'translated'),
		('Rebirth in a Perfect Era',       'Rebirth in a Perfect Era',                      'translated'),
		('Immortal',                       'Immortal',                                      'translated'),
		('Great Tyrannical Deity',         'Great Tyrannical Deity',                        'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False