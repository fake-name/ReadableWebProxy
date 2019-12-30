def extractSoraTranslations(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'teaser' in item['title'].lower():
		return False
	if 'Isekai Mahou....' in item['tags']:
		return buildReleaseMessageWithType(item, 'Isekai Mahou wa Okureteru!', vol, chp, frag=frag, postfix=postfix)
	return False
