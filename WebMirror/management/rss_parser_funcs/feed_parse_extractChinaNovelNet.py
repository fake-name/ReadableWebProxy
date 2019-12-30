def extractChinaNovelNet(item):
	"""
	China Novel.net
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if item['title'].startswith('Shura’s Wrath Chapter'):
		return buildReleaseMessageWithType(item, 'Shura’s Wrath', vol, chp, frag=frag, postfix=postfix)
	return False
