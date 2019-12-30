def extractA0132(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if chp or vol:
		return buildReleaseMessageWithType(item, 'Terror Infinity', vol, chp, frag=frag, postfix=postfix)
	return False
