def extractHamster428(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Mei Gongqing' in item['tags']:
		return buildReleaseMessageWithType(item, 'Mei Gongqing', vol, chp, frag=frag, postfix=postfix)
	return False
