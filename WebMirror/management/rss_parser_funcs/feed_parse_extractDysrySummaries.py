def extractDysrySummaries(item):
	"""
	Dysry Summaries
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Summary' in item['tags']:
		return None
	return False
