def extractCrazedplanetWordpressCom(item):
	'''
	Parser for 'crazedplanet.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('life after marrying my love rival',         'life after marrying my love rival',                        'translated'),
		('Who Dares Slander My Senior Brother',       'Who Dares Slander My Senior Brother',                      'translated'),
		('Can You Connect to Your Wifi?',             'Can You Connect to Your Wifi?',                            'translated'),
		('Taizi',                                     'Taizi',                                                    'translated'),
		('can i connect to your wifi?',               'can i connect to your wifi?',                              'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False