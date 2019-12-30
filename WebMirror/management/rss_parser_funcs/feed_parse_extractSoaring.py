def extractSoaring(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'teaser' in item['title'].lower():
		return False
	if 'Limitless Sword God Chapter' in item['title'] or 'Limitless Sword God' in item['tags'] or 'LSG' in item['tags']:
		return buildReleaseMessageWithType(item, 'Limitless Sword God', vol, chp, frag=frag, postfix=postfix)
	return False
