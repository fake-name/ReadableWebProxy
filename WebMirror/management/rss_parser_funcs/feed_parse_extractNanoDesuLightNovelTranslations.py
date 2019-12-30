def extractNanoDesuLightNovelTranslations(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Ore to Kawazu-san no Isekai Hourouki' in item['tags']:
		return buildReleaseMessageWithType(item, 'Ore to Kawazu-san no Isekai Hourouki', vol, chp, frag=frag, postfix=postfix)
	return False
