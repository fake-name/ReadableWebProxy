def extractTriangleNovels(item):
	'''
	Parser for 'Triangle Novels'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if "WFTT" in item['tags']:
		return buildReleaseMessageWithType(item, "Waiting For The Train", vol, chp, frag=frag, postfix=postfix)
	if "AFGITMOLFM" in item['tags']:
		return buildReleaseMessageWithType(item, "AFGITMOLFM", vol, chp, frag=frag, postfix=postfix)

	return False