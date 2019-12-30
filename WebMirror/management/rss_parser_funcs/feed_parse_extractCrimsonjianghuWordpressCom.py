def extractCrimsonjianghuWordpressCom(item):
	'''
	Parser for 'crimsonjianghu.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
	
	if item['title'].startswith("Chapter "):
		return buildReleaseMessageWithType(item, "Elite Hidden Marriage: Black Bellied President dotes on Wife", vol, chp, frag=frag, postfix=postfix)
	

	return False