def extractPeachknightWordpressCom(item):
	'''
	Parser for 'peachknight.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('sozai saishu',       'Isekai Nonbiri Sozai Saishu Seikatsu',                      'translated'),
		('sozaisaishu',       'Isekai Nonbiri Sozai Saishu Seikatsu',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False