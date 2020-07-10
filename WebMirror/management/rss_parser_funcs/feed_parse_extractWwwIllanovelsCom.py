def extractWwwIllanovelsCom(item):
	'''
	Parser for 'www.illanovels.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('my little happiness',       'my little happiness',                      'translated'),
		('intense love',              'intense love',                             'translated'),
		('Under the Power',           'Under the Power',                          'translated'),
		('Unrequited Love',           'Unrequited Love',                          'translated'),
		('Autumn\'s Concerto',        'Autumn\'s Concerto',                       'translated'),
		('the love equations',        'the love equations',                       'translated'),
		('love is sweet',             'love is sweet',                            'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False