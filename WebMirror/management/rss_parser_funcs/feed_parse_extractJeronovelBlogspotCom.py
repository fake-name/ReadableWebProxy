def extractJeronovelBlogspotCom(item):
	'''
	Parser for 'jeronovel.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Books to Dominate Married Women',       'Books to Dominate Married Women',                      'translated'),
		('Only Ero knowledge',                    'I Have The Only Ero Knowledge In The World',           'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False