def extractFirebirdsNest(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'no-fatigue' in item['tags']:
		return buildReleaseMessageWithType(item, 'No Fatigue', vol, chp, frag=frag, postfix=postfix)
	if 'mondaiji' in item['tags']:
		return buildReleaseMessageWithType(item, 'Mondaiji-tachi ga Isekai Kara Kuru Sou Desu yo?', vol, chp, frag=frag, postfix=postfix)
	return False
