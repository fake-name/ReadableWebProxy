def extract閒人ONLINE(item):
	"""
	閒人 • O N L I N E
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Great Tang Idyll' in item['tags']:
		return buildReleaseMessageWithType(item, 'Great Tang Idyll', vol, chp, frag=frag, postfix=postfix)
	return False
