def extractOtakutlBlogspotCom(item):
	'''
	Parser for 'otakutl.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('the record of barton\'s fantastical events',    'the record of barton\'s fantastical events',                   'translated'),
		('TRO',                                           'The Rise of Otaku',                                            'translated'),
		('the rise of otaku',                             'The Rise of Otaku',                                            'translated'),
		('Dark Blood Age',                                'Dark Blood Age',                                               'translated'),
		('psfilwm',                                       'Problematic Sister Fell In Love With Me',                      'translated'),
		('porblematic sister fell in love with me',       'Problematic Sister Fell In Love With Me',                      'translated'),
		('world apocalypse online',                       'world apocalypse online',                                      'translated'),
		('STH',                                           'Shrouding the Heavens',                                        'translated'),
		('Shrouding the Heavens',                         'Shrouding the Heavens',                                        'translated'),
		('history\'s top sect leader',                    'history’s top sect leader',                                    'translated'),
		('history’s top sect leader',                     'history’s top sect leader',                                    'translated'),
		('son',                                           'soul of negary',                      'translated'),
		('soul of negary',                                'soul of negary',                      'translated'),
		('ecltd',                                         'every confession leads to death',                      'translated'),
		('every confession leads to death',               'every confession leads to death',                      'translated'),
		('cultivate your sister',                         'cultivate your sister',                                        'translated'),
		('sword immortal in another world',               'sword immortal in another world',                              'translated'),
		('driver of the beautiful ceo',                   'driver of the beautiful ceo',                                  'translated'),
		('i really didn\'t want to become a system',      'i really didn\'t want to become a system',                     'translated'),
		('purvaviheda\'s tale of sealing demons',         'purvaviheda\'s tale of sealing demons',                        'translated'),
		('wasteland employment guide',                    'wasteland employment guide',                                   'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False