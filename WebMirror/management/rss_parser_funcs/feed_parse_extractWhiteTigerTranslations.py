def extractWhiteTigerTranslations(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if item['title'].lower().startswith('mp volume'):
		return buildReleaseMessageWithType(item, 'Martial Peak', vol, chp, frag=frag, postfix=postfix)
	if item['title'].lower().startswith('ipash chapter'):
		return buildReleaseMessageWithType(item, 'Martial Peak', vol, chp, frag=frag, postfix=postfix)
	return False
