def extractAlexanderwalesCom(item):
	'''
	Parser for 'alexanderwales.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('PRC',       'PRC',                      'translated'),
		('worth the candle',           'worth the candle',                          'oel'),
		('the dark wizard of donkerk', 'the dark wizard of donkerk',                'oel'),
		('Glimwarden',                 'Glimwarden',                                'oel'),
		('Shadows of the Limelight',   'Shadows of the Limelight',                  'oel'),
		('The Last Christmas',         'The Last Christmas',                        'oel'),
		('a bluer shade of white',     'a bluer shade of white',                    'oel'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False