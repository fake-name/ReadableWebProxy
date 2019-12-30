def extractLightNovelCafe(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Evolution Theory of the Hunter' in item['tags']:
		return buildReleaseMessageWithType(item, 'Evolution Theory of the Hunter', vol, chp, frag=frag, postfix=postfix)
	if "God's Song" in item['tags']:
		return buildReleaseMessageWithType(item, "God's Song", vol, chp, frag=frag, postfix=postfix)
	if 'Life Mission' in item['tags']:
		return buildReleaseMessageWithType(item, 'Life Mission', vol, chp, frag=frag, postfix=postfix)
	return False
