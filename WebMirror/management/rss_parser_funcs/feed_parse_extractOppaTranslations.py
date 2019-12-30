def extractOppaTranslations(item):
	"""
	'OppaTranslations'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	tagmap = [
		('Main Character Hides His Strength',               'Main Character Hides His Strength',                              'translated'), 
		('mchhs',                                           'Main Character Hides His Strength',                              'translated'), 
		('Master Hunter K',                                 'Master Hunter K',                                                'translated'), 
		('Chemistry',                                       'Chemistry',                                                      'translated'), 
		('Chemi',                                           'Chemistry',                                                      'translated'), 
		('poten',                                           'poten',                                                          'translated'),
		('colossus hunter',                                 'colossus hunter',                                                'translated'),
		
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
	return False