def extractEnTruceTranslations(item):
	"""
	# EnTruce Translations

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'kuro no maou' in item['title'].lower() and 'chapter' in item['title'].lower() and (chp or vol):
		return buildReleaseMessageWithType(item, 'Kuro no Maou', vol, chp, frag=frag, postfix=postfix)
	if 'kuro no maou' in item['tags'] and (chp or vol):
		return buildReleaseMessageWithType(item, 'Kuro no Maou', vol, chp, frag=frag, postfix=postfix)
	if 'maken no daydreamer' in item['tags'] and (chp or vol):
		return buildReleaseMessageWithType(item, 'Maken no Daydreamer', vol, chp, frag=frag, postfix=postfix)
	if 'knw' in item['tags'] and (chp or vol):
		return buildReleaseMessageWithType(item, 'Konjiki no Wordmaster', vol, chp, frag=frag, postfix=postfix)
	return False
