def extractYuritranslationsWordpressCom(item):
	'''
	Parser for 'yuritranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('qt abused female lead and beautiful villainess',       'QT Abused Female Lead and Beautiful Villainess',                      'translated'),
		('pregnant with the villain boss\' baby',                'pregnant with the villain boss\' baby',                               'translated'),
		('how luck i am to meet you',                            'how lucky i am to meet you',                                          'translated'),
		('she is the protagonist',                               'she is the protagonist',                                              'translated'),
		('never dare to abuse the female lead again',            'never dare to abuse the female lead again',                           'translated'),
		('abused female lead and beautiful villainess',          'abused female lead and beautiful villainess',                         'translated'),
		('my consort is an alpha',                               'my consort is an alpha',                                              'translated'),
		('my feelings can wait',                                 'my feelings can wait',                                                'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False