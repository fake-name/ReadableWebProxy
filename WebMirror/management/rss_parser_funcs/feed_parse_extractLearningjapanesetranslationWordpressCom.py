def extractLearningjapanesetranslationWordpressCom(item):
	'''
	Parser for 'learningjapanesetranslation.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('kikanshita yuusha',                     'Kikanshita Yuusha no Gojitsudan',                      'translated'),
		('kikanshita yuusha no gojitsudan',       'Kikanshita Yuusha no Gojitsudan',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False