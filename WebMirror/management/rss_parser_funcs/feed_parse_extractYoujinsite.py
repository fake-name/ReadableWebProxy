def extractYoujinsite(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if '[God & Devil World]' in item['tags'] and (chp or vol):
		return buildReleaseMessageWithType(item, 'Shenmo Xitong', vol, chp, frag=frag, postfix=postfix)
	if '[LBD&A]' in item['tags'] and (chp or vol):
		return buildReleaseMessageWithType(item, 'Line between Devil and Angel', vol, chp, frag=frag, postfix=postfix)
	if '[VW: Conquer the World]' in item['tags'] and (chp or vol):
		return buildReleaseMessageWithType(item, 'VW: Conquering the World', vol, chp, frag=frag, postfix=postfix)
	return False
