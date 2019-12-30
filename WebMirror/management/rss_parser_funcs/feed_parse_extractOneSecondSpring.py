def extractOneSecondSpring(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'The Princess Who Cannot Marry' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Princess Who Cannot Marry', vol, chp, frag=frag, postfix=postfix)
	if 'Heavy Sweetness Ash-like Frost' in item['tags']:
		return buildReleaseMessageWithType(item, 'Heavy Sweetness Ash-like Frost', vol, chp, frag=frag, postfix=postfix)
	if 'Our Second Master' in item['tags']:
		return buildReleaseMessageWithType(item, 'Our Second Master', vol, chp, frag=frag, postfix=postfix)
	return False
