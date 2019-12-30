def extractTLSyosetsu(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if item['title'].lower().strip().startswith('defiled hero chapter'):
		return buildReleaseMessageWithType(item, 'Defiled Hero', vol, chp, frag=frag, postfix=postfix)
	return False
