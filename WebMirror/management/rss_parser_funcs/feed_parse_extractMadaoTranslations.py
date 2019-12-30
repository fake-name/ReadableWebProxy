def extractMadaoTranslations(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'My Death Flags Show No Sign of Ending' in item['tags']:
		chp, frag = frag, chp
		return buildReleaseMessageWithType(item, 'Ore no Shibou Flag ga Todomaru Tokoro wo Shiranai', vol, chp, frag=frag, postfix=postfix)
	return False
