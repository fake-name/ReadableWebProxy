def extractLittlemonster8HomeBlog(item):
	'''
	Parser for 'littlemonster8.home.blog'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('the chronicle of the oriole island',       'the chronicle of the oriole island',                      'translated'),
		('jin wang dotes on his concubine',          'jin wang dotes on his concubine',                         'translated'),
		('fight for peace and love',                 'fight for peace and love',                                'translated'),
		('love story at starry night',               'love story at starry night',                              'translated'),
		('未分类',                                   'Sunset Boulevard',                                        'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False