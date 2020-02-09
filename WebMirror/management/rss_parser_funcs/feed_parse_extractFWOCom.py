def extractFWOCom(item):
	'''
	Parser for 'f-w-o.com'
	'''

	
	badwords = [
			'paywalled',
			'VIP subscriptions',
		]
	if any([bad in item['title'] for bad in badwords]):
		return None



	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('A Cheeky Kendo God',                                        'A Cheeky Kendo God',                                                       'translated'),
		('Those Years When We Killed the White Lotus',                'Those Years When We Killed the White Lotus',                               'translated'),
		('Conquest',                                                  'Conquest',                                                                 'translated'),
		('watch me eat fish it\'s exciting!',                         'watch me eat fish it\'s exciting!',                                        'translated'),
		('I can download',                                            'I can download',                                                           'translated'),
		('raising dragons in hollywood',                              'raising dragons in hollywood',                                             'translated'),
		('travel to a primitive world to build infrastructure',       'travel to a primitive world to build infrastructure',                      'translated'),
		('Midnight Cinderella',                                       'Midnight Cinderella',                                                      'translated'),
		('the last cat in the universe',                              'the last cat in the universe',                                             'translated'),
		('genius fundamentals',                                       'Genius Fundamentals',                                                      'translated'),
		('ancient rome: from slaveholder to supreme emperor',         'ancient rome: from slaveholder to supreme emperor',                        'translated'),
		('Apocalyptic Rebirth: Earth’s Vast Changes',                 'Apocalyptic Rebirth: Earth’s Vast Changes',                                'translated'),
		('watch me eat fish',                                         'Watch me eat fish it’s exciting!',                                         'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False