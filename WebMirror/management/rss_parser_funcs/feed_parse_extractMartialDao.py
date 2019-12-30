def extractMartialDao(item):
	"""
	Martial Dao
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if item['title'].startswith('Awakening Chap'):
		return buildReleaseMessageWithType(item, 'Awakening', vol, chp, frag=frag, postfix=postfix)
	if item['title'].startswith('Shadow Rogue'):
		return buildReleaseMessageWithType(item, 'Shadow Rogue', vol, chp, frag=frag, postfix=postfix)
	if item['title'].startswith('The Almight Martial Arts System Chap') or item['title'].startswith('The Almighty Martial Arts System Chap'):
		return buildReleaseMessageWithType(item, 'The Almighty Martial Arts System', vol, chp, frag=frag, postfix=postfix)
	return False
