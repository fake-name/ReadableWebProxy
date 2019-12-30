def extractKumaOtou(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if "I Kinda Came to Another World but where's the way home" in item['tags'] and 'translation' in item['tags']:
		return buildReleaseMessageWithType(item, 'Isekai Kichattakedo Kaerimichi doko?', vol, chp, frag=frag, postfix=postfix)
	return False
