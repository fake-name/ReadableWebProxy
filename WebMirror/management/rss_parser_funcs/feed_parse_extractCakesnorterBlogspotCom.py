def extractCakesnorterBlogspotCom(item):
	'''
	Parser for 'cakesnorter.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('back to before i married the tyrant',       'Back to Before I Married the Tyrant [Rebirth]',                      'translated'),
		('bbmt',                                      'Back to Before I Married the Tyrant [Rebirth]',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False