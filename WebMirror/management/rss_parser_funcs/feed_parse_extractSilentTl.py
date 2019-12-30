def extractSilentTl(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Legend' in item['tags']:
		return buildReleaseMessageWithType(item, 'Legend', vol, chp, frag=frag, postfix=postfix)
	return False
