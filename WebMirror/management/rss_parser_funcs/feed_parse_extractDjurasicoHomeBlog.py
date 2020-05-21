def extractDjurasicoHomeBlog(item):
	'''
	Parser for 'djurasico.home.blog'
	'''
	
	

	badwords = [
			'light novels français',
			'badword',
		]
	if any([bad in item['tags'] for bad in badwords]):
		return None



	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('the duchess of the attic',                         'The Duchess of the attic',                                        'translated'),
		('Garudeina Oukoku Koukoku Ki',                      'Garudeina Oukoku Koukoku Ki',                                     'translated'),
		('The Noble Girl Living in Debt',                    'The Noble Girl Living in Debt',                                   'translated'),
		('the duchess of rosia -a contract marriage?',       'the duchess of rosia -a contract marriage?',                      'translated'),
		('loved by her sister’s former fiancée',             'loved by her sister’s former fiancée',                            'translated'),
		('31st consort candidate',                           '31st consort candidate',                                          'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False