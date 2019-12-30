def extractWigglyTranslation(item):
	"""
	Wiggly Translation
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if item['title'].startswith('Man Huang Feng Bao: '):
		return buildReleaseMessageWithType(item, 'Man Huang Feng Bao', vol, chp, frag=frag, postfix=postfix)
	return False
