def extractWwwThenovelstCom(item):
	'''
	Parser for 'www.thenovelst.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Reincarnation – Lord is Extremely Hardcore',       'Reincarnation – Lord is Extremely Hardcore',                      'translated'),
		('If You Are a Dodder Flower',                       'If You Are a Dodder Flower',                                      'translated'),
		('Legend of Hua Buqi',                               'Legend of Hua Buqi',                                              'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False