def extractTotallyInsaneTranslation(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'PMG' in item['tags']:
		return buildReleaseMessageWithType(item, 'Peerless Martial God', vol, chp, frag=frag, postfix=postfix)
	if 'DtH' in item['tags']:
		return buildReleaseMessageWithType(item, 'Devouring The Heavens', vol, chp, frag=frag, postfix=postfix)
	return False
