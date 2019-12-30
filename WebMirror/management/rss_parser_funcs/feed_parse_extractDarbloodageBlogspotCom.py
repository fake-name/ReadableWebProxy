def extractDarbloodageBlogspotCom(item):
	'''
	Parser for 'darbloodage.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	if item['tags'] == [] and item['title'].lower().startswith("chapter "):
		return buildReleaseMessageWithType(item, "Dark Blood Age", vol, chp, frag=frag, postfix=postfix)

	return False