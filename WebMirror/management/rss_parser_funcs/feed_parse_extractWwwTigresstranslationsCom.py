def extractWwwTigresstranslationsCom(item):
	'''
	Parser for 'www.tigresstranslations.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Enemy!',                     'I Will Not Become an Enemy!',                                       'translated'),
		('Two Saints',                 'Two Saints wander off into a Different World',                      'translated'),
		('Only with Your Heart',       'Only with Your Heart',                                              'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False