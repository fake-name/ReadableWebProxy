def extractPettankoTranslations(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if item['title'].startswith('Isekai C-mart Hanjouki'):
		return buildReleaseMessageWithType(item, 'Isekai C-mart Hanjouki', vol, chp, frag=frag, postfix=postfix)
	return False
