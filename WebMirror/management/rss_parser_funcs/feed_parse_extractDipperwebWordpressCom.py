def extractDipperwebWordpressCom(item):
	'''
	Parser for 'dipperweb.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	if item['tags'] == ['translation'] and item['title'].startswith("Chapter "):
		return buildReleaseMessageWithType(item, "Inner Demons", vol, chp, frag=frag, postfix=postfix)

	if item['title'].startswith("Inner Demons "):
		return buildReleaseMessageWithType(item, "Inner Demons", vol, chp, frag=frag, postfix=postfix)

	return False