def extractPeachblossomdreamsHomeBlog(item):
	'''
	Parser for 'peachblossomdreams.home.blog'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('aggrievedfishsprite',       'Yu Bu Fu: Aggrieved Fish Sprite',                      'translated'),
		('teie',                      'The Emperor is Expecting!',                            'translated'),
		('bfss',                      'Blooming Flowers, Silent Sorrow',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False