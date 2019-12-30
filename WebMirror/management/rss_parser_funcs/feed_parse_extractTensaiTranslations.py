def extractTensaiTranslations(item):
	"""
	# Tensai Translations

	"""
	chp, vol, frag = extractChapterVolFragment(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Spirit Migration' in item['tags']:
		return buildReleaseMessageWithType(item, 'Spirit Migration', vol, chp, frag=frag)
	if 'Tsuyokute New Saga' in item['tags']:
		return buildReleaseMessageWithType(item, 'Tsuyokute New Saga', vol, chp, frag=frag)
	return False
