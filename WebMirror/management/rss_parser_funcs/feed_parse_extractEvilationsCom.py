def extractEvilationsCom(item):
	'''
	Parser for 'evilations.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('TQBCT',                                          'Top Quality Beauty Cultivation Technique',                      'translated'),
		('Top Quality Beauty Cultivation Technique',       'Top Quality Beauty Cultivation Technique',                      'translated'),
		('OA',                                             'Overgod Ascension',                                             'translated'),
		('Overgod Ascension',                              'Overgod Ascension',                                             'translated'),
		('MCIA',                                           'My Consort Is Alpha',                                           'translated'),
		('My Consort Is Alpha',                            'My Consort Is Alpha',                                           'translated'),
		('VPAATP',                                         'Very Pure and Ambiguous: The Prequel',                          'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False