def extractWatermelonHelmets(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Dragon Life' in item['tags'] or 'Dragon Life: Chapter' in item['title']:
		return buildReleaseMessageWithType(item, 'Dragon Life', vol, chp, frag=frag, postfix=postfix)
	return False
