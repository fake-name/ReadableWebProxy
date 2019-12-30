def extractKerambit(item):
	"""
	# Kerambit's Incisions

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Yobidasa' in item['tags'] and (vol or chp):
		if not postfix and ':' in item['title']:
			postfix = item['title'].split(':')[-1]
		return buildReleaseMessageWithType(item, 'Yobidasareta Satsuriku-sha', vol, chp, frag=frag, postfix=postfix)
	return False
