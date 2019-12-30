def extractNowhereNothing(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'The Undying Cultivator' in item['tags']:
		if vol != None:
			return
		if 'Arc 1: A Monster Inside' in item['tags']:
			return buildReleaseMessageWithType(item, 'The Undying Cultivator', 1, chp, frag=frag, postfix=postfix, tl_type='oel')
		if 'Arc 2: Courting Death' in item['tags']:
			return buildReleaseMessageWithType(item, 'The Undying Cultivator', 2, chp, frag=frag, postfix=postfix, tl_type='oel')
	if item['title'].startswith('While We Slept '):
		if vol != None:
			return
		return buildReleaseMessageWithType(item, 'Nowhere & Nothing', 1, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False
