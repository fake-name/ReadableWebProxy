def extractWalkingTheStorm(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	return buildReleaseMessageWithType(item, 'Joy of life', vol, chp, frag=frag, postfix=postfix)
