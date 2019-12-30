def extractCabnovelsWordpressCom(item):
	'''
	Parser for 'cabnovels.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	if "xi ling empire" in item['tags']:
		return buildReleaseMessageWithType(item, "Xyrin Empire", vol, chp, frag=frag, postfix=postfix)
	if item['title'].startswith("XE "):
		return buildReleaseMessageWithType(item, "Xyrin Empire", vol, chp, frag=frag, postfix=postfix)
	if item['title'].startswith("(Ch."):
		return buildReleaseMessageWithType(item, "Xyrin Empire", vol, chp, frag=frag, postfix=postfix)

	return False