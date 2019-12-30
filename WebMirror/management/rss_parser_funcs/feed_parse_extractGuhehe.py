def extractGuhehe(item):
	"""
	# guhehe.TRANSLATIONS

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'ShominSample' in item['tags']:
		return buildReleaseMessageWithType(item, 'Ore ga Ojou-sama Gakkou ni "Shomin Sample" Toshite Rachirareta Ken', vol, chp, frag=frag, postfix=postfix)
	if 'OniAi' in item['tags']:
		return buildReleaseMessageWithType(item, 'Onii-chan Dakedo Ai Sae Areba Kankeinai yo ne', vol, chp, frag=frag, postfix=postfix)
	if 'Haganai' in item['tags']:
		return buildReleaseMessageWithType(item, 'Boku wa Tomodachi ga Sukunai', vol, chp, frag=frag, postfix=postfix)
	return False
