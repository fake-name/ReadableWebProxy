def extractSmoggytranslatesCom(item):
	'''
	Parser for 'smoggytranslates.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('i transmigrated into a stunning plaything!',       'i transmigrated into a stunning plaything!',                      'translated'),
		('taking my elder brothers as husbands',             'taking my elder brothers as husbands',                            'translated'),
		('ivory moonlight',                                  'ivory moonlight',                                                 'translated'),
		('The Men at Her Feet',                              'The Men at Her Feet',                                             'translated'),
		('anti-cheater strategies',                          'anti-cheater strategies',                                         'translated'),
		('the imperial doctor belongs to the princess',      'the imperial doctor belongs to the princess',                     'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False