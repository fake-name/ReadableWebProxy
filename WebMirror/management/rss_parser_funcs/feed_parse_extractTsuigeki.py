def extractTsuigeki(item):
	"""
	# Tsuigeki Translations

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Seiju no Kuni no Kinju Tsukai' in item['tags'] and (chp or vol):
		return buildReleaseMessageWithType(item, 'Seiju no Kuni no Kinju Tsukai', vol, chp, frag=frag, postfix=postfix)
	return False
