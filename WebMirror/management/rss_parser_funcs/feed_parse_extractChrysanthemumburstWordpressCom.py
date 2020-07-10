def extractChrysanthemumburstWordpressCom(item):
	'''
	Parser for 'chrysanthemumburst.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('ASV',                                           'a smile from the villain',                                     'translated'),
		('a smile from the villain',                      'a smile from the villain',                                     'translated'),
		('r:dsat',                                        'rebirth: degenerate slave abuses tyrant',                      'translated'),
		('rebirth: degenerate slave abuses tyrant',       'rebirth: degenerate slave abuses tyrant',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False