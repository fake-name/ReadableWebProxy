def extractLevityTales(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if item['title'].startswith('Overthrowing Fate'):
		return buildReleaseMessageWithType(item, 'Overthrowing Fate', vol, chp, frag=frag, postfix=postfix)
	if item['title'].startswith('Ancient Godly Monarch'):
		return buildReleaseMessageWithType(item, 'Ancient Godly Monarch', vol, chp, frag=frag, postfix=postfix)
	if 'Chaotic Lightning Cultivation' in item['tags']:
		return buildReleaseMessageWithType(item, 'Chaotic Lightning Cultivation', vol, chp, frag=frag, postfix=postfix)
	if 'Overthrowing Fate' in item['tags']:
		return buildReleaseMessageWithType(item, 'Overthrowing Fate', vol, chp, frag=frag, postfix=postfix)
	return False
