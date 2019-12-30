def extractPenguTaichou(item):
	"""
	Pengu Taichou
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if item['title'].lower().startswith('sword shisho chapter'):
		return buildReleaseMessageWithType(item, 'I was a Sword when I Reincarnated!', vol, chp, frag=frag, postfix=postfix)
	return False
