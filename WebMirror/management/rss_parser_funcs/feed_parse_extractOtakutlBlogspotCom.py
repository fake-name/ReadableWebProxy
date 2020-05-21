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
		('world apocalypse online',       'world apocalypse online',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False