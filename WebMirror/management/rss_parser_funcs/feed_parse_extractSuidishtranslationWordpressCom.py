def extractSuidishtranslationWordpressCom(item):
	'''
	Parser for 'suidishtranslation.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
	
	if chp == 9999999999:
		return None

	tagmap = [
		('Going Back and Forth Between Earth and The Other World with Space Time Magic',       'Going Back and Forth Between Earth and The Other World with Space Time Magic',                      'translated'),
		('HP9999999999',                                                                       'HP9999999999',                                                                                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False