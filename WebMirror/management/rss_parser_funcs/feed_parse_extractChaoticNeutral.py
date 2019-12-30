def extractChaoticNeutral(item):
	"""
	Parser for 'Chaotic Neutral'
	"""
	if 'asks' in item['tags']:
		return None
	if 'reblog' in item['tags']:
		return None
		
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'WATTT' in item['tags']:
		return buildReleaseMessageWithType(item, 'WATTT', vol, chp, frag=frag, postfix=postfix)
	return False