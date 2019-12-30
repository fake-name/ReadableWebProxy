def extractBijinsans(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Benkyou no Kamisama wa Hitomishiri' in item['tags']:
		return buildReleaseMessageWithType(item, 'Benkyou no Kamisama wa Hitomishiri', vol, chp, frag=frag, postfix=postfix)
	return False
