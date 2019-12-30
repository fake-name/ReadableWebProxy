def extractExtantVisions(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	if 'Lily Ex Machina' in item['tags']:
		return buildReleaseMessageWithType(item, 'Lily Ex Machina', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'Seeking Elysium' in item['tags']:
		return buildReleaseMessageWithType(item, 'Seeking Elysium', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
		
	return False