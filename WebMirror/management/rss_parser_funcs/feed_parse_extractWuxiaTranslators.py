def extractWuxiaTranslators(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'World Defying Dan God' in item['tags']:
		return buildReleaseMessageWithType(item, 'World Defying Dan God', vol, chp, frag=frag, postfix=postfix)
	return False
