def extractMahoutsuki(item):
	"""
	# Mahoutsuki Translation

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Uncategorized' in item['tags'] and chp and ('Chapter' in item['title'] or 'prologue' in item['title']):
		return buildReleaseMessageWithType(item, 'Le Festin de Vampire', vol, chp, frag=frag, postfix=postfix)
	return False
