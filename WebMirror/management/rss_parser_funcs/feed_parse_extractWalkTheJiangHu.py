def extractWalkTheJiangHu(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'TTNH Chapter' in item['title']:
		return buildReleaseMessageWithType(item, 'Transcending the Nine Heavens', vol, chp, frag=frag, postfix=postfix)
	return False
