def extractRamdomtlBlogspotCom(item):
	'''
	Parser for 'ramdomtl.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('mayojou',       'The Chronicles of a Lost Man in His Forties Founding a Nation ~Commonsense is Hindering Me From Becoming TUEE~',                      'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	return False