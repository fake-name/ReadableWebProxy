def extractPositivelyaddictedWordpressCom(item):
	'''
	Parser for 'positivelyaddicted.wordpress.com'
	'''
	
	
	badwords = [
			'Link',
		]
	if any([bad in item['tags'] for bad in badwords]):
		return None



	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Bringing a Son to Marry A Giant',          'Bringing a Son to Marry A Giant',                         'translated'),
		('Tianting Kindergarten',                    'Tianting Kindergarten',                                   'translated'),
		('Ti Shen (Body Double)',                    'Ti Shen',                                                 'translated'),
		('PRC',                                      'PRC',                                                     'translated'),
		('The Flower Under Heaven Blooms with Love', 'The Flower Under Heaven Blooms with Love',                'oel'),
		('Dragon Child',                             'Tales of Ea: Dragon Child',                               'oel'),
		('Loiterous',                                'Loiterous',                                               'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False