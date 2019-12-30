def extractExMachinaAsia(item):
	"""
	ExMachina.Asia
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	if 'Ultimate Assassin System' in item['tags']:
		return buildReleaseMessageWithType(item, 'Ultimate Assassin System', vol, chp, frag=frag, postfix=postfix)
	if "We live in dragon's peak" in item['tags']:
		return buildReleaseMessageWithType(item, "We live in dragon's peak", vol, chp, frag=frag, postfix=postfix)
		
	return False