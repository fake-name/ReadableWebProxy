def extractRrrrhexiatranslationHomeBlog(item):
	'''
	Parser for 'rrrrhexiatranslation.home.blog'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Flower',                               'Childish Flower',                                                         'translated'),
		('The villain is too beautiful',         'The villain is too beautiful',                                            'translated'),
		('Those Years I Operated a Zoo',         'Those Years I Operated a Zoo',                                            'translated'),
		('I have a Secret',                      'I have a Secret',                                                         'translated'),
		('zoo',                                  'Those Years I Operated a Zoo',                                            'translated'),
		('Secret',                               'I Have A Secret (Fast Wear)',                                             'translated'),
		('Brushing Boss',                        'After Brushing the Apocalypse\'s Boss for 363 Days',                      'translated'),
		('villain',                              'The Villain Is Too Beautiful',                                            'translated'),
		('Responsible',                          'I Don\'t Want You To Be Responsible',                                     'translated'), 
		('brushing boss for 363 days',           'After Brushing the Apocalypse\'s Boss for 363 Days',                      'translated'), 
		('i don\'t want you to be responsible',  'I Don\'t Want You To Be Responsible!',                                    'translated'), 
		('become a koi and fall into male god\'s bathtub',       'become a koi and fall into male god\'s bathtub',                      'translated'), 
		('encountering a snake',                                 'encountering a snake',                                                'translated'), 
		('PRC',       'PRC',                      'translated'), 
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	if item['tags'] == ['Announcement']:
		titlemap = [
			('363D – ',           'After Brushing the Apocalypse\'s Boss for 363 Days',                      'translated'), 
			('IDWYR – ',          'I Don\'t Want You To Be Responsible!',                                    'translated'), 
		]

		for titlecomponent, name, tl_type in titlemap:
			if titlecomponent.lower() in item['title'].lower():
				return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False