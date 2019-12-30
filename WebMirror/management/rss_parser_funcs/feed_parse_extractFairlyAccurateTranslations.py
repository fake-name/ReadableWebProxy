def extractFairlyAccurateTranslations(item):
	"""
	Fairly Accurate Translations
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if item['title'].lower().startswith('card disciple – chapter'):
		return buildReleaseMessageWithType(item, 'Card Disciple', vol, chp, frag=frag, postfix=postfix)
	if 'Card Disciple' in item['tags']:
		return buildReleaseMessageWithType(item, 'Card Disciple', vol, chp, frag=frag, postfix=postfix)
	return False
