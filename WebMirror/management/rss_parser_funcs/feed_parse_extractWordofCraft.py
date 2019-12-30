def extractWordofCraft(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Toaru Ossan no VRMMO katsudouki' in item['tags']:
		return buildReleaseMessageWithType(item, 'Toaru Ossan no VRMMO katsudouki', vol, chp, frag=frag, postfix=postfix)
	return False
