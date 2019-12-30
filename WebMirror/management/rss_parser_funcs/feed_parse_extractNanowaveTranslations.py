def extractNanowaveTranslations(item):
	"""

	"""
	titletmp = item['title'].replace("'High Speed! 2:", '')
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(titletmp)
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'high speed! 2 translation' in item['tags']:
		return buildReleaseMessageWithType(item, 'High Speed!', vol, chp, frag=frag, postfix=postfix)
	return False
