def extractGrandlation(item):
	"""
	Grandlation
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'DMWG' in item['tags']:
		return buildReleaseMessageWithType(item, 'Dragon-Marked War God', vol, chp, frag=frag, postfix=postfix)
	if item['title'].startswith('DMWG Chapter'):
		return buildReleaseMessageWithType(item, 'Dragon-Marked War God', vol, chp, frag=frag, postfix=postfix)
	if item['title'].startswith('Yang God Chapter'):
		return buildReleaseMessageWithType(item, 'Yang God', vol, chp, frag=frag, postfix=postfix)
	return False
