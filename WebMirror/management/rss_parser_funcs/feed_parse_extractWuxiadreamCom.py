def extractWuxiadreamCom(item):
	'''
	Parser for 'wuxiadream.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Douluo Continent 2.5 - Legend of The Divine Realm',       'Douluo Continent 2.5 - Legend of The Divine Realm', 'translated'),
		('The Legend of Eternal Night\'s Sovereign',                'The Legend of Eternal Night\'s Sovereign',          'translated'),
		('Ghost: "Catch the ghost!"',                               'Ghost: "Catch the ghost!"',                         'translated'),
		('Repugnant Gateway',                                       'Repugnant Gateway',                                 'translated'),
		('The Master\'s Legend',                                    'The Master\'s Legend',                              'translated'),
		('Douluo Continent',                                        'Douluo Continent',                                  'translated'),
		('God of Slaughter',                                        'God of Slaughter',                                  'translated'),
		('Card Disciple',                                           'Card Disciple',                                     'translated'),
		('King of Myriad Domain',                                   'King of Myriad Domain',                             'translated'),
		('Imperial God Emperor',                                    'Imperial God Emperor',                              'translated'),
		('Monarch of Eternal Night',                                'Monarch of Eternal Night',                          'translated'),
		('Eternal Night\'s Sovereign',                              'Eternal Night\'s Sovereign',                        'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False