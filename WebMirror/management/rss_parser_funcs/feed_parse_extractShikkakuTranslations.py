def extractShikkakuTranslations(item):
	"""
	# Shikkaku Translations

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'kuro no maou' in item['title'].lower():
		return buildReleaseMessageWithType(item, 'Kuro no Maou', vol, chp, frag=frag, postfix=postfix)
	if 'KENS' in item['tags']:
		return buildReleaseMessageWithType(item, 'Kamigoroshi no Eiyuu to Nanatsu no Seiyaku', vol, chp, frag=frag, postfix=postfix)
	return False
