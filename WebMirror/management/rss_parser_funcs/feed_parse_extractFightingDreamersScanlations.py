def extractFightingDreamersScanlations(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Light Novel' in item['tags'] and 'Slayers Special' in item['tags']:
		return buildReleaseMessageWithType(item, 'Slayers Special', vol, chp, frag=frag, postfix=postfix)
	return False
