def extractSolitaryTranslation(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'The Great Ruler' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Great Ruler', vol, chp, frag=frag, postfix=postfix)
	return False
