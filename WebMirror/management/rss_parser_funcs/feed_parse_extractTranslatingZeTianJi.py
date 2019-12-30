def extractTranslatingZeTianJi(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	return buildReleaseMessageWithType(item, 'Ze Tian Ji ', vol, chp, frag=frag, postfix=postfix)
