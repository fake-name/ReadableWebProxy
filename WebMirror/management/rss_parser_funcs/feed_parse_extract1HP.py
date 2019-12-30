def extract1HP(item):
	"""
	# 1HP

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Route to almightyness from 1HP' in item['title'] and (chp or vol):
		return buildReleaseMessageWithType(item, 'HP1 kara Hajimeru Isekai Musou', vol, chp, frag=frag, postfix=postfix)
	return False
