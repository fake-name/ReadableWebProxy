def extractNovelsnowCom(item):
	'''
	Parser for 'novelsnow.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	tagmap = [
		('My Sister the Heroine and I the Villainess',       'My Sister the Heroine, and I the Villainess',                      'translated'),
		('My Sister the Heroine',                            'My Sister the Heroine, and I the Villainess',                      'translated'),
		('Sage Ruler',                                       'Sage Emperor',                                                     'translated'),   # Typo?
		('Sage Emperor',                                     'Sage Emperor',                                                     'translated'),
		('Super soldier',                                    'Super soldier',                                                    'translated'),
		('MG',                                               'Dragon Emperor, Martial God',                                      'translated'),
		('martial god',                                      'Dragon Emperor, Martial God',                                      'translated'),
		('Dragon Emperor',                                   'Dragon Emperor, Martial God',                                      'translated'),
		('Wang Ye Captures His Wife',                        'Wang Ye Captures His Wife',                                        'translated'),
		('Blacksmith',                                       'Expecting to Fall into Ruin, I Aim to Become a Blacksmith',        'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	return False