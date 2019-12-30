def extractTsukigomori(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag):
		return False
	if 'Our Glamorous Time' in item['tags']:
		return buildReleaseMessageWithType(item, 'Our Glamorous Time', vol, chp, frag=frag, postfix=postfix)
	if 'Same Place Not Same Bed' in item['tags']:
		return buildReleaseMessageWithType(item, 'Same Place Not Same Bed', vol, chp, frag=frag, postfix=postfix)
	return False
