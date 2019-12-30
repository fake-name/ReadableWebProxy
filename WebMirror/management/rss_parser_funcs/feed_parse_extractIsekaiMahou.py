def extractIsekaiMahou(item):
	"""
	# Isekai Mahou Translations!

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Isekai Mahou Chapter' in item['title'] and 'Release' in item['title']:
		return buildReleaseMessageWithType(item, 'Isekai Mahou wa Okureteru!', vol, chp, frag=frag, postfix=postfix)
	return False
