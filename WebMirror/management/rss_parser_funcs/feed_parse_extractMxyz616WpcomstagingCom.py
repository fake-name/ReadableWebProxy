def extractMxyz616WpcomstagingCom(item):
	'''
	Parser for 'mxyz616.wpcomstaging.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('let me go! i need to study!',        'let me go! i need to study!',                       'translated'),
		('My Disciple Consumes Too Much',      'My Disciple Consumes Too Much',                     'translated'),
		('mary sue meets cinderella',          'mary sue meets cinderella',                         'translated'),
		('female lead is a black lotus',       'female lead is a black lotus',                      'translated'),
		('for the rest of our life',           'for the rest of our life',                          'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False