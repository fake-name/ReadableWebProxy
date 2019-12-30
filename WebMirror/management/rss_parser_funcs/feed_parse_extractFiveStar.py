def extractFiveStar(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Xian Ni' in item['title']:
		return buildReleaseMessageWithType(item, 'Xian Ni', vol, chp, frag=frag, postfix=postfix)
	return False
