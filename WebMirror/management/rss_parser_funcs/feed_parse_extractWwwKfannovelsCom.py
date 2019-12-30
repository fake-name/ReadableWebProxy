def extractWwwKfannovelsCom(item):
	'''
	Parser for 'www.kfannovels.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Limit Breaker',                                'Limit Breaker',                                               'translated'),
		('All Stat Slayer',                              'All Stat Slayer',                                             'translated'),
		('Dragon\'s Legacy',                             'Dragon\'s Legacy',                                            'translated'),
		('Accumulate Experience by Reading Books',       'Accumulate Experience by Reading Books',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False