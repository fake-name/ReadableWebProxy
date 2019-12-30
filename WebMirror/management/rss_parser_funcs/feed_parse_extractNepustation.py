def extractNepustation(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Cheat Majutsu' in item['tags']:
		return buildReleaseMessageWithType(item, 'Cheat Majutsu De Unmei Wo Nejifuseru', vol, chp, frag=frag, postfix=postfix)
	return False
