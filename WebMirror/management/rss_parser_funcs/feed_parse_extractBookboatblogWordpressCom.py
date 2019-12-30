def extractBookboatblogWordpressCom(item):
	'''
	Parser for 'bookboatblog.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	if "Haroon" in item['tags']:
		return buildReleaseMessageWithType(item, "Haroon", vol, chp, frag=frag, postfix=postfix)

	return False