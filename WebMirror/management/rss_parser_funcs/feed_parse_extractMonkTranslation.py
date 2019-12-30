def extractMonkTranslation(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Battle Emperor' in item['tags']:
		return buildReleaseMessageWithType(item, 'Battle Emperor', vol, chp, frag=frag, postfix=postfix)
	return False
