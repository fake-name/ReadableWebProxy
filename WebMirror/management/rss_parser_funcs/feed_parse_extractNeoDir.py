def extractNeoDir(item):
	"""
	Parser for 'Neo DIR'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Wicked Soldier King' in item['tags']:
		return buildReleaseMessageWithType(item, 'Wicked Soldier King', vol, chp, frag=frag, postfix=postfix)
	if 'Very Pure Very Vague' in item['tags']:
		return buildReleaseMessageWithType(item, 'Very Pure Very Vague', vol, chp, frag=frag, postfix=postfix)
	if 'Very pure very ambiguous' in item['tags']:
		return buildReleaseMessageWithType(item, 'Very Pure and Ambiguous: The Prequel', vol, chp, frag=frag, postfix=postfix)
	return False