def extractAiHristDreamTranslations(item):
	"""
	'Ai Hrist Dream Translations'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	tagmap = [
		('Godly Farmer Doctor: Arrogant husband, can\'t afford to offend!',       'Godly Farmer Doctor: Arrogant husband, can\'t afford to offend!',                      'translated'),
		('One Child Two Treasures: The Billionaire Chief’s Good Wife',            'One Child Two Treasures: The Billionaire Chief’s Good Wife',                           'translated'),
		('Good Morning, Mr. President!',                                          'Good Morning, Mr. President!',                                                         'translated'),
		('Princess Medical Doctor',                                               'Princess Medical Doctor',                                                              'translated'),
		('Into the World of Medicine',                                            'Into the World of Medicine',                                                           'translated'),
		('Ghost Marriage, the abandoned wife has three treasures',                'Ghost Marriage, the abandoned wife has three treasures',                               'translated'),
		('fortune teller master',                                                 'fortune teller master',                                                                'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
	return False