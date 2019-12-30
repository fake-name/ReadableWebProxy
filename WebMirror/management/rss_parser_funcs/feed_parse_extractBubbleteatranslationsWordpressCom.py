def extractBubbleteatranslationsWordpressCom(item):
	'''
	Parser for 'bubbleteatranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Ice Lord Prime Minister\'s Black-Bellied Wife',       'Ice Lord Prime Minister\'s Black-Bellied Wife',                      'translated'),
		('ILPMBBW',                                             'Ice Lord Prime Minister\'s Black-Bellied Wife',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False