def extractBerryMtl(item):
	'''
	Parser for 'Berry MTL'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if "I Can Speak to Animals and Demons" in item['tags']:
		return buildReleaseMessageWithType(item, "I Can Speak to Animals and Demons", vol, chp, frag=frag, postfix=postfix)

	return False