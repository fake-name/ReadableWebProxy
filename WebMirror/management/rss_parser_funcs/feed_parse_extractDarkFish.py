def extractDarkFish(item):
	"""
	# DarkFish Translations

	"""
	chp, vol, frag = extractChapterVolFragment(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'She Professed Herself The Pupil Of The Wise Man'.lower() in item['title'].lower() or 'She Professed Herself The Pupil Of The Wise Man'.lower() in [tmp.lower() for
	    tmp in item['tags']]:
		return buildReleaseMessageWithType(item, 'Kenja no Deshi wo Nanoru Kenja', vol, chp, frag=frag)
	return False
