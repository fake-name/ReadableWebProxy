def extractSnowTimeTranslations(item):
	"""
	SnowTime Translations
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'In Different World With Naruto System' in item['tags']:
		return buildReleaseMessageWithType(item, 'In Different World With Naruto System', vol, chp, frag=frag, postfix=postfix)
	return False
