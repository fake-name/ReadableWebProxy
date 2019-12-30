def extractGoddessGrantMeaGirlfriend(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'ggmag chapter' in item['tags']:
		return buildReleaseMessageWithType(item, 'Goddess! Grant Me a Girlfriend!!', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False
