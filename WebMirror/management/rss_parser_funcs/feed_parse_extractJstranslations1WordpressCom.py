def extractJstranslations1WordpressCom(item):
	'''
	Parser for 'jstranslations1.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [        
		('ordered to marry thrice, the mysterious wangfei',               'ordered to marry thrice, the mysterious wangfei',                             'translated'),
		('rebirth of the general’s granddaughter',                        'rebirth of the general’s granddaughter',                                      'translated'),
		('you can’t be fierce towards me!',                               'you can’t be fierce towards me!',                                             'translated'),
		('rebirth of the abandoned woman: godly doctor taizi fei',        'rebirth of the abandoned woman: godly doctor taizi fei',                      'translated'),
		('Being An Author Is A High Risk Occupation',                     'Being An Author Is A High Risk Occupation',                                   'translated'),
		('one hundred ways to become a god',                              'one hundred ways to become a god',                                            'translated'),
		('Every World Seems Not Quite Right',                             'Every World Seems Not Quite Right',                                           'translated'),
		('seizing a good marriage, the virtuous medical consort',         'seizing a good marriage, the virtuous medical consort',                       'translated'),
		('rebirth of a counterattack: godly doctor shizi fei',            'rebirth of a counterattack: godly doctor shizi fei',                          'translated'),
		('congratulations, empress',                                      'congratulations, empress',                                                    'translated'),
		('descent of the phoenix – 13-year-old princess consort',         'descent of the phoenix – 13-year-old princess consort',                       'translated'),
		('Rebirth of the Marquis’ Di Daughter',                           'Rebirth of the Marquis’ Di Daughter',                                         'translated'),
		('young master jun’s 100 techniques to spoil his wife',           'young master jun’s 100 techniques to spoil his wife',                         'translated'),
		('secret service princess: the cold prince’s black belly wife',   'secret service princess: the cold prince’s black belly wife',                 'translated'),
		('PRC',        'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False