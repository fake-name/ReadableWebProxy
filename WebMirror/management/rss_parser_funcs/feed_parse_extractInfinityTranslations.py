def extractInfinityTranslations(item):
	"""
	'Infinity Translations'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'ETC' in item['tags']:
		return buildReleaseMessageWithType(item, 'Emperor of The Cosmos', vol, chp, frag=frag, postfix=postfix)
	if 'SAS' in item['tags']:
		return buildReleaseMessageWithType(item, 'Strongest Abandoned Son', vol, chp, frag=frag, postfix=postfix)
	if 'Disb' in item['tags']:
		return buildReleaseMessageWithType(item, 'Death is The Beginning', vol, chp, frag=frag, postfix=postfix)
	return False
