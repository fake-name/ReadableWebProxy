def extractEhmedtranslationsWordpressCom(item):
	'''
	Parser for 'ehmedtranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Almighty Student',                               'Almighty Student',                                              'translated'),
		('The Primordial Throne',                          'The Primordial Throne',                                         'translated'),
		('Very Pure and Ambiguous',                        'Very Pure and Ambiguous',                                       'translated'),
		('Overgod Ascension',                              'Overgod Ascension',                                             'translated'),
		('Top Quality Beauty Cultivation Technique',       'Top Quality Beauty Cultivation Technique',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False