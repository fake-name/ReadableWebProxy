def extractTsundereOjisan(item):
	'''
	Parser for 'Tsundere ojisan'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if "Kuro no senki" in item['tags']:
		return buildReleaseMessageWithType(item, "Kuro no Senki", vol, chp, frag=frag, postfix=postfix)

	return False