def extractFreeimaginationrealmWordpressCom(item):
	'''
	Parser for 'freeimaginationrealm.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('major general\'s smart and gorgeous wife',           'Major General\'s Smart and Gorgeous Wife',                      'translated'),
		('the major general\'s smart and gorgeous wife',       'Major General\'s Smart and Gorgeous Wife',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False