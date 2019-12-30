def extractLazycatnovelsWordpressCom(item):
	'''
	Parser for 'lazycatnovels.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Mighty Female Official',                               'Mighty Female Official',                                              'translated'),
		('Xiaobei\'s Life as a Proud and Respected Woman',       'Xiaobei\'s Life as a Proud and Respected Woman',                      'translated'),
		('the world\'s number one den of iniquity',              'The World\'s No. 1 Den of Iniquity',                                  'translated'),
		('the world\'s number one brothel',                      'The World\'s No. 1 Den of Iniquity',                                  'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False