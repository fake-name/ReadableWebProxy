def extractAlcsel(item):
	"""
	# 'Alcsel Translations'

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'AR Chapter' in item['title']:
		return buildReleaseMessageWithType(item, 'Assassin Reborn', vol, chp, frag=frag, postfix=postfix)
	return False
