def extractPriddlesTranslations(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Magic is Japanese' in item['tags']:
		return buildReleaseMessageWithType(item, 'Magic is Japanese', vol, chp, frag=frag, postfix=postfix)
	return False
