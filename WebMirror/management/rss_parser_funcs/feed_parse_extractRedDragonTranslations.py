def extractRedDragonTranslations(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Kaettekite mo fantasy' in item['tags']:
		return buildReleaseMessageWithType(item, 'Kaettekite mo Fantasy!?', vol, chp, frag=frag, postfix=postfix)
	return False
