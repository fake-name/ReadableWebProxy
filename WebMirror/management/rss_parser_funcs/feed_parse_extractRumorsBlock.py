def extractRumorsBlock(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if "Rumor's Block" in item['tags'] and 'chapter' in item['title'].lower():
		return buildReleaseMessageWithType(item, "Rumor's Block", vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False
