def extractAltorocTranslations(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Shadow Rogue' in item['tags']:
		return buildReleaseMessageWithType(item, 'Shadow Rogue', vol, chp, frag=frag, postfix=postfix)
	return False
