def extractPockysbookshelfBlogspotCom(item):
	'''
	Parser for 'pockysbookshelf.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Methods to Save the Villain who was Abandoned by the Heroine',       'Methods to Save the Villain who was Abandoned by the Heroine',                      'translated'),
		('If I Happened to Tame my Brother Well',                              'If I Happened to Tame my Brother Well',                                             'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False