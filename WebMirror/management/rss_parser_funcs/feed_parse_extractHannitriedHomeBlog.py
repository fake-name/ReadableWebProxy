
def extractHannitriedHomeBlog(item):
	'''
	Parser for 'hannitried.home.blog'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return _buildReleaseMessage(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False
	