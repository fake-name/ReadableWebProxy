def extractLimostnWordpressCom(item):
	'''
	Parser for 'limostn.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	if "The Outcast" in item['tags']:
		return buildReleaseMessageWithType(item, "The Outcast", vol, chp, frag=frag, postfix=postfix)

	return False