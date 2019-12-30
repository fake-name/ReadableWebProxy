def extractFaketypist(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'The Magician wants Normality' in item['tags']:
		return buildReleaseMessageWithType(item, 'Madoushi wa Heibon wo Nozomu', vol, chp, frag=frag, postfix=postfix)
	return False
