def extractWillfulCasual(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Chu Wang Fei' in item['tags']:
		return buildReleaseMessageWithType(item, 'Chu Wang Fei', vol, chp, frag=frag, postfix=postfix)
	return False
