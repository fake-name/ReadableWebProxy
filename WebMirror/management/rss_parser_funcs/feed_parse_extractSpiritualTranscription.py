def extractSpiritualTranscription(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'TEO' in item['tags'] or 'The Empyrean Overlord' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Empyrean Overlord', vol, chp, frag=frag, postfix=postfix)
	return False
