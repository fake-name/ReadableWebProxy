def extractEasyDesignBlog(item):
	'''
	Parser for 'easy.design.blog'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('-Yuri War-',       'Yuri War of the Demon King\'s Daughter – the Brave Hero Who Incarnates as the Ts Wants to Protect a Peaceful Life Surrounded by Cute Demons and Monster Girls',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False