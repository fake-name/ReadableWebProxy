def extractWCCTranslation(item):
	"""
	# WCC Translation

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if 'chapter' in item['title'].lower():
		if ':' in item['title']:
			postfix = item['title'].split(':', 1)[-1]
		return buildReleaseMessageWithType(item, 'World Customize Creator', vol, chp, frag=frag, postfix=postfix)
	return False
