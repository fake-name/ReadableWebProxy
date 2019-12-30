def extractOKTranslation(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Oyaji Kanojo' in item['tags']:
		return buildReleaseMessageWithType(item, 'Oyaji Kanojo', vol, chp, frag=frag, postfix=postfix)
	return False
