def extractRosyFantasy(item):
	"""

	"""
	
	badwords = [
			'review',
		]
	if any([bad in item['tags'] for bad in badwords]):
		return None


	
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None

	tagmap = [
		('Yu Ren',                                                'Yu Ren',                                          'translated'),
		('Chu Wang Fei',                                          'Chu Wang Fei',                                    'translated'),
		('Seven Unfortunate Lifetimes',                           'Seven Unfortunate Lifetimes',                     'translated'),
		('All Thanks to a Single Moment of Impulse',              'All Thanks to a Single Moment of Impulse',        'translated'),
		('White Calculation',                                     'White Calculation',                               'translated'),
		("demon wang's gold medal status favorite fei",           "Demon Wang's Golden Favorite Fei",                'translated'),
		("demon's wang golden favorite fei",                      "Demon Wang's Golden Favorite Fei",                'translated'),
		("emperor is in trouble again",                           "emperor is in trouble again",                     'translated'),
		("seeking happiness",                                     "Seeking Happiness",                               'translated'),
		("living up to you",                                      "living up to you",                                'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	if item['title'].startswith('DWGMSFF'):
		return buildReleaseMessageWithType(item, "Demon Wang's Golden Favorite Fei", vol, chp, frag=frag, postfix=postfix)
		
	return False