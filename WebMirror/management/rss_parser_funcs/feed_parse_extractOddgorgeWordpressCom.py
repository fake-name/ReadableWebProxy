def extractOddgorgeWordpressCom(item):
	'''
	Parser for 'oddgorge.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	if "General Above I am Below" in item['tags']:
		return buildReleaseMessageWithType(item, "General Above I am Below", vol, chp, frag=frag, postfix=postfix)

	return False