def extractGaochaoTranslations(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Otherworldly Evil Monarch' in item['tags']:
		return buildReleaseMessageWithType(item, 'Otherworldly Evil Monarch', vol, chp, frag=frag, postfix=postfix)
	return False
