def extractCeruleonice(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'martial emperor reborn' in item['tags']:
		return buildReleaseMessageWithType(item, 'Martial Emperor Reborn', vol, chp, frag=frag, postfix=postfix)
	if 'Totem' in item['tags']:
		return buildReleaseMessageWithType(item, 'Totem', vol, chp, frag=frag, postfix=postfix)
	return False
