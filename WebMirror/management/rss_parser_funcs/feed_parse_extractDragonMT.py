def extractDragonMT(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Dragon Life' in item['tags']:
		return buildReleaseMessageWithType(item, 'Dragon Life', vol, chp, frag=frag, postfix=postfix)
	return False
