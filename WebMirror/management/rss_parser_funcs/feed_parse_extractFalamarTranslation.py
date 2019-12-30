def extractFalamarTranslation(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Isekai ni kanaderu densetsu' in item['tags']:
		return buildReleaseMessageWithType(item, 'Isekai ni kanaderu densetsu ~toki wo tomeru mono~', vol, chp, frag=frag, postfix=postfix)
	if 'The road to become a transition master in another world' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Road to Become a Transition Master in Another World', vol, chp, frag=frag, postfix=postfix)
	return False
