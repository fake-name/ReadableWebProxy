def extractManga0205Translations(item):
	"""
	# Manga0205 Translations

	"""
	chp, vol, frag = extractChapterVolFragment(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Sendai Yuusha wa Inkyou Shitai'.lower() in item['title'].lower():
		postfix = ''
		if 'Side Story'.lower() in item['title'].lower():
			postfix = 'Side Story {num}'.format(num=chp)
			chp = None
		return buildReleaseMessageWithType(item, 'Sendai Yuusha wa Inkyou Shitai', vol, chp, frag=frag, postfix=postfix)
	return False
