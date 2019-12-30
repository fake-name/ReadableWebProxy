def extractGrimdarkZTranslations(item):
	"""
	# 'GrimdarkZ Translations'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Devouring The Heavens' in item['tags']:
		return buildReleaseMessageWithType(item, 'Devouring The Heavens', vol, chp, frag=frag, postfix=postfix)
	if 'Kuro no Hiera Glaphicos' in item['tags']:
		return buildReleaseMessageWithType(item, 'Kuro no Hiera Glaphicos', vol, chp, frag=frag, postfix=postfix)
	return False
