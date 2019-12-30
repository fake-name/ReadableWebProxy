def extractAeongardenWordpressCom(item):
	'''
	Parser for 'aeongarden.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('A Sequel For The Villainess',                       'A Sequel For The Villainess',                                      'translated'),
		('Otome Game no Akuyaku Reijou o Tanoshimitai',       'Otome Game no Akuyaku Reijou o Tanoshimitai',                      'translated'),
		('Heikinten no Reijou',                               'Heikinten no Reijou',                                              'translated'),
		('Mouichido Aeta Nara, Ippai no Egao o',              'Mouichido Aeta Nara, Ippai no Egao o',                             'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False