def extractTransnovelationWordpressCom(item):
	'''
	Parser for 'transnovelation.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Mr. Dior',                           'Mr. Dior',                                          'translated'),
		('I Dare You To Run Away Again',       'I Dare You To Run Away Again',                      'translated'),
		('Jun Ye Can\'t Help But Tease His Wife',       'Jun Ye Can\'t Help But Tease His Wife',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False