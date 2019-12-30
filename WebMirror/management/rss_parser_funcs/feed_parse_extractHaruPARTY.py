def extractHaruPARTY(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Yuusha Party' in item['tags']:
		return buildReleaseMessageWithType(item, 'Yuusha Party no Kawaii Ko ga Ita no de, Kokuhaku Shite', vol, chp, frag=frag, postfix=postfix)
	return False
