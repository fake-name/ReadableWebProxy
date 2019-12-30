def extractIdyllicTranslations(item):
	"""
	Idyllic Translations
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Dragon Long Long' in item['tags']:
		return buildReleaseMessageWithType(item, 'Dragon Long Long', vol, chp, frag=frag, postfix=postfix)
	return False
