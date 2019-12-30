def extractDawningHowls(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Dragon Flies Phoenix Dances' in item['tags']:
		return buildReleaseMessageWithType(item, 'Dragon Flies Phoenix Dances', vol, chp, frag=frag, postfix=postfix)
	if 'Eastern Palace' in item['tags']:
		return buildReleaseMessageWithType(item, 'Eastern Palace', vol, chp, frag=frag, postfix=postfix)
	return False
