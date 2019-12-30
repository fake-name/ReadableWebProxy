def extractAmaryllideaetranslationsWordpressCom(item):
	'''
	Parser for 'amaryllideaetranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('BYBOTE',                                                  'Begging You to Break Off This Engagement!',                              'translated'),
		('Begging You to Break Off This Engagement!',               'Begging You to Break Off This Engagement!',                              'translated'),
		('Yang Shu Mei Ying',                                       'Yang Shu Mei Ying',                                                      'translated'),
		('Bring Along a Ball and Hiding from Foreign Devils',       'Bring Along a Ball and Hiding from Foreign Devils',                      'translated'),
		('Aloof King and Cool-Acting Queen',                        'Aloof King and Cool-Acting Queen',                                       'translated'),
		('Feng Mang',                                               'Feng Mang',                                                              'translated'),
		('The Wife is First',                                       'The Wife is First',                                                      'translated'),
		('Blood Contract',                                          'Blood Contract',                                                         'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False