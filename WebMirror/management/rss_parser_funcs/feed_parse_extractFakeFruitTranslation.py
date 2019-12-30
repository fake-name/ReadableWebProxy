def extractFakeFruitTranslation(item):
	"""
	Fake Fruit Translation
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Bringing the Supermarket to the Apocalypse' in item['tags']:
		return buildReleaseMessageWithType(item, 'Bringing the Supermarket to the Apocalypse', vol, chp, frag=frag, postfix=postfix)
	return False
