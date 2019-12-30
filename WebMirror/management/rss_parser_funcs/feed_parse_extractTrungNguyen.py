def extractTrungNguyen(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Bringing the Farm to Live in Another World' in item['title'] or 'Bringing the Farm...' in item['title']:
		return buildReleaseMessageWithType(item, 'Bringing the Farm to Live in Another World', vol, chp, frag=frag, postfix=postfix)
	if 'The First Alchemist - Chap' in item['title']:
		return buildReleaseMessageWithType(item, 'The First Alchemist', vol, chp, frag=frag, postfix=postfix)
	return False
