def extractYoushoku(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if 'The Other World Dining Hall' in item['tags'] and (chp or vol):
		return buildReleaseMessageWithType(item, 'The Other World Dining Hall', vol, chp, frag=frag, postfix=postfix)
	return False
