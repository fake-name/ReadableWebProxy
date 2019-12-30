def extractSilverliningtranslationsWordpressCom(item):
	'''
	Parser for 'silverliningtranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	if item['title'].startswith("Skeleton Knight "):
		return buildReleaseMessageWithType(item, "Skeleton Knight, in Another World", vol, chp, frag=frag, postfix=postfix)

	return False