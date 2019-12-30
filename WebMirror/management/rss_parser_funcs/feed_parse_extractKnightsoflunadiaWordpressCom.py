def extractKnightsoflunadiaWordpressCom(item):
	'''
	Parser for 'knightsoflunadia.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	if "OR" in item['tags']:
		return buildReleaseMessageWithType(item, "Ouroboros Records", vol, chp, frag=frag, postfix=postfix)

	return False