def extractTrippTl(item):
	"""
	# Tripp Translations

	"""
	chp, vol, frag = extractChapterVolFragment(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Majin Tenseiki' in item['title']:
		return buildReleaseMessageWithType(item, 'Majin Tenseiki', vol, chp, frag=frag)
	return False
