def extractLovelikeathousandarrowsWordpressCom(item):
	'''
	Parser for 'lovelikeathousandarrows.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('green plum fairy road',       'green plum fairy road',                      'translated'),
		('the eternal heavenly dao system of ten thousand realms',       'the eternal heavenly dao system of ten thousand realms',                      'translated'),
		('the super special forces king',       'the super special forces king',                      'translated'),
		('urban strenghtening system',       'urban strenghtening system',                      'translated'),
		('super special forces king',        'super special forces king',                       'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False