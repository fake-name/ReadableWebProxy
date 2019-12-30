def extractZSW(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if 'Shen Mu' in item['tags'] and (chp or vol):
		return buildReleaseMessageWithType(item, 'Shen Mu', vol, chp, frag=frag, postfix=postfix)
	return False
