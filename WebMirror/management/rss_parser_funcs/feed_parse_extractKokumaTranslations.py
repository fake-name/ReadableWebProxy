def extractKokumaTranslations(item):
	"""
	'Kokuma Translations'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if item['tags'] == ['Uncategorized'] and item['title'].startswith('Arena Chapter'):
		return buildReleaseMessageWithType(item, 'Arena', vol, chp, frag=frag, postfix=postfix)
	return False
