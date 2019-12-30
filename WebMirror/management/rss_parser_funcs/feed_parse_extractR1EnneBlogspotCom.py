def extractR1EnneBlogspotCom(item):
	'''
	Parser for 'r1enne.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	if "Inner Demons" in item['tags']:
		return buildReleaseMessageWithType(item, "Inner Demons", vol, chp, frag=frag, postfix=postfix)
	
	if item['title'].startswith("Chapter "):
		return buildReleaseMessageWithType(item, "Inner Demons", vol, chp, frag=frag, postfix=postfix)
	
	return False