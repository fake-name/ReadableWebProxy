def extractPeonynoveltlBlogspotCom(item):
	'''
	Parser for 'peonynoveltl.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('one hundred ways to become a god',      'One hundred ways to become God',                       'translated'),
		('a cat with a red envelope group',       'A cat with a red envelope group',                      'translated'),
		('holding on to my man',                  'Holding on to my man',                                 'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False