def extractHyorinmaruBlog(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if item['title'].lower().strip().startswith('martial world – ') or 'Martial World' in item['tags']:
		return buildReleaseMessageWithType(item, 'Martial World', vol, chp, frag=frag, postfix=postfix)
	return False
