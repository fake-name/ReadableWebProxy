def extractPalmtreehBlogspotCom(item):
	'''
	Parser for 'palmtreeh.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Don\'t Turn from Summer 莫负寒夏',        'Don\'t Turn from Summer',                      'translated'),
		('Don\'t Turn from Summer  莫负寒夏',       'Don\'t Turn from Summer',                      'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False