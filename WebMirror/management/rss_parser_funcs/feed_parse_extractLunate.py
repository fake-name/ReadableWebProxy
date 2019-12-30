def extractLunate(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if 'chapter' in item['title'].lower() and (vol or chp):
		return buildReleaseMessageWithType(item, 'World Customize Creator', vol, chp, frag=frag, postfix=postfix)
	return False
