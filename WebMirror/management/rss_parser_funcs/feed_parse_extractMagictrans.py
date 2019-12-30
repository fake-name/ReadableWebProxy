def extractMagictrans(item):
	"""
	Magictrans
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Release that Witch' in item['tags']:
		return buildReleaseMessageWithType(item, 'Release that Witch', vol, chp, frag=frag, postfix=postfix)
	return False
