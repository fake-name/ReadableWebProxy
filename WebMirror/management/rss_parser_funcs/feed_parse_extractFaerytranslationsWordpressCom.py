def extractFaerytranslationsWordpressCom(item):
	'''
	Parser for 'faerytranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('bnddsb',                                          'brother next door, don\'t sleep on my bed',                      'translated'),
		('brother next door, don\'t sleep on my bed',       'brother next door, don\'t sleep on my bed',                      'translated'),
		('DS',                                              'demon\'s sweetheart',                      'translated'),
		('demon\'s sweetheart',                             'demon\'s sweetheart',                      'translated'),
		('trwnla',                                          'the rich woman is no longer acting',                      'translated'),
		('the rich woman is no longer acting',              'the rich woman is no longer acting',                      'translated'),
		('tvreg',                                           'the villain\'s reborn ex-girlfriend',                      'translated'),
		('the villain\'s reborn ex-girlfriend',             'the villain\'s reborn ex-girlfriend',                      'translated'),
		('sdwz',                                            'splendid dream of wanzhou',                      'translated'),
		('splendid dream of wanzhou',                       'splendid dream of wanzhou',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False