def extractCloudtranslatesWordpressCom(item):
	'''
	Parser for 'cloudtranslates.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('heart of glass',                    'Heart of Glass',                                   'translated'),
		('Breaking through the Clouds',       'Breaking through the Clouds',                      'translated'),
		('ISMM',                              'I Ship My Adversary X Me',                         'translated'),
		('I Ship My Adversary X Me',          'I Ship My Adversary X Me',                         'translated'),
		('SW',                                'Slow-Witted',                                      'translated'),
		('Slow-Witted',                       'Slow-Witted',                                      'translated'),
		('LRotPB',                            'Lantern: Reflection of the Peach Blossoms',        'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False