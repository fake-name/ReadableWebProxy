def extractRisingDragons(item):
	"""
	# Rising Dragons Translation

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'God and Devil World' in item['tags'] and 'Release' in item['tags']:
		return buildReleaseMessageWithType(item, 'Shenmo Xitong', vol, chp, frag=frag, postfix=postfix)
	return False
