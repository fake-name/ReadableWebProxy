def extractWuxiaTranslations(item):
	"""
	# Wuxia Translations

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	releases = ['A Martial Odyssey', 'Law of the Devil', 'Tensei Shitara Slime Datta Ken', 'The Nine Cauldrons', 'Sovereign of the Three Realms']
	for name in releases:
		if name in item['title'] and (chp or vol):
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix)
	return False
