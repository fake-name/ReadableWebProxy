def extractECWebnovel(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if item['title'].lower().startswith('volume'):
		return buildReleaseMessageWithType(item, 'EC', vol, chp, frag=frag, postfix=postfix)
	if item['title'].lower().startswith('great merchant - dao ming'):
		return buildReleaseMessageWithType(item, 'Great Merchant - Dao Ming', vol, chp, frag=frag, postfix=postfix)
	return False
