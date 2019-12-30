def extractTranslationRaven(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Godly Hunter' in item['tags']:
		return buildReleaseMessageWithType(item, 'Godly Hunter', vol, chp, frag=frag, postfix=postfix)
	return False
