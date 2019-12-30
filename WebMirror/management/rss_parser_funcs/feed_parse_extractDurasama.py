def extractDurasama(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Arifureta' in item['tags']:
		return buildReleaseMessageWithType(item, 'Arifureta', vol, chp, frag=frag, postfix=postfix)
	if 'Manuke FPS' in item['tags']:
		return buildReleaseMessageWithType(item, 'Manuke na FPS Player ga isekai e ochita baai', vol, chp, frag=frag, postfix=postfix)
	return False
