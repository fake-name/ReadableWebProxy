def extractBinggoCorp(item):
	"""
	# Binggo & Corp Translations

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Jiang Ye' in item['title'] and 'Chapter' in item['title']:
		return buildReleaseMessageWithType(item, 'Jiang Ye', vol, chp, frag=frag, postfix=postfix)
	if 'Ze Tian Ji' in item['title'] and 'Chapter' in item['title']:
		return buildReleaseMessageWithType(item, 'Ze Tian Ji', vol, chp, frag=frag, postfix=postfix)
	return False
