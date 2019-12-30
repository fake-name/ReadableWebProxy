def extractFungShen(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Shrouded' in item['tags']:
		return buildReleaseMessageWithType(item, 'Shrouded', vol, chp, frag=frag, postfix=postfix)
	return False
