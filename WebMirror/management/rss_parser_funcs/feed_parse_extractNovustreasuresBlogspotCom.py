def extractNovustreasuresBlogspotCom(item):
	'''
	Parser for 'novustreasures.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Xuan Wang Above Di Daughter Runs Away',       'Xuan Wang Above Di Daughter Runs Away',                                      'translated'),
		('The Aloof Prince',                            'The Aloof Prince Pampers his Wild First Rate Consort!',                      'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False