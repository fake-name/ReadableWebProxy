def extractCalicoxTabby(item):
	"""
	# Calico x Tabby

	"""
	chp, vol, frag = extractChapterVolFragment(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Meow Meow Meow' in item['tags']:
		return buildReleaseMessageWithType(item, 'Meow Meow Meow', vol, chp, frag=frag)
	return False
