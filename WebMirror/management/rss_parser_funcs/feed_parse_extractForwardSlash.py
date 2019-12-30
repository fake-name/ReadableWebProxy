def extractForwardSlash(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Isekai ni Demodori Shimashita?' in item['tags']:
		return buildReleaseMessageWithType(item, 'Isekai ni Demodori Shimashita?', vol, chp, frag=frag, postfix=postfix)
	return False
