def extractSteadyTranslation(item):
	"""
	Steady Translation
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Online Game: Evil Dragon Against The Heaven' in item['tags']:
		return buildReleaseMessageWithType(item, 'Online Game: Evil Dragon Against The Heaven', vol, chp, frag=frag, postfix=postfix)
	if 'In Different World With Naruto System' in item['tags']:
		return buildReleaseMessageWithType(item, 'In Different World With Naruto System', vol, chp, frag=frag, postfix=postfix)
	if 'The Alchemist God' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Alchemist God', vol, chp, frag=frag, postfix=postfix)
	return False
