def extractBuBuJingXinTrans(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if 'bu bu jing xin' in item['tags'] and (chp or vol):
		return buildReleaseMessageWithType(item, 'Bu Bu Jing Xin', vol, chp, frag=frag, postfix=postfix)
	return False
