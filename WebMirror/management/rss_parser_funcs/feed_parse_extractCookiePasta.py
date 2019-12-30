def extractCookiePasta(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	return buildReleaseMessageWithType(item, 'Douluo Dalu 2 - Jueshi Tangmen', vol, chp, frag=frag, postfix=postfix)
