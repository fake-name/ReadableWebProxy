def extractForgottenConqueror(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if chp:
		return buildReleaseMessageWithType(item, 'Forgotten Conqueror', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False
