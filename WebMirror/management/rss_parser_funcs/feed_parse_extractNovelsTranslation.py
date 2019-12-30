def extractNovelsTranslation(item):
	"""
	Novels Translation
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Womanizing Mage' in item['tags']:
		return buildReleaseMessageWithType(item, 'Womanizing Mage', vol, chp, frag=frag, postfix=postfix)
	return False
