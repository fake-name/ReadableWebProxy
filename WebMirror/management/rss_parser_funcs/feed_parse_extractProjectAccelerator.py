def extractProjectAccelerator(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Black Healer' in item['tags']:
		return buildReleaseMessageWithType(item, 'Black Healer', vol, chp, frag=frag, postfix=postfix)
	return False
