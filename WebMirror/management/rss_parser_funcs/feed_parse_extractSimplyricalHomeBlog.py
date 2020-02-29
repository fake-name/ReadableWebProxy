def extractSimplyricalHomeBlog(item):
	'''
	Parser for 'simplyrical.home.blog'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		(';black eagle saint',      'Black Eagle’s Saint~ The Expelled Healer Masters Dark Magic from His Spare Magic Powers',                      'translated'),
		('black eagle saint',       'Black Eagle’s Saint~ The Expelled Healer Masters Dark Magic from His Spare Magic Powers',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False