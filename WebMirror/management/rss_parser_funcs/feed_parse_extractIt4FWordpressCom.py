def extractIt4FWordpressCom(item):
	'''
	Parser for 'it4f.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
	
	tagset = set(item['tags'])
	
	if tagset == set(["Uncategorized", "Adventure", "Fiction", "Fantasy"]) and item['title'].startswith("Chapter "):
		return buildReleaseMessageWithType(item, 'Devil’s Son-In-Law', vol, chp, frag=frag, postfix=postfix)
	

	return False