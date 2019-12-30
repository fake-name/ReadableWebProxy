def extractNeetTranslations(item):
	"""
	# NEET Translations

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Marginal Operation' in item['tags']:
		return buildReleaseMessageWithType(item, 'Marginal Operation', vol, chp, frag=frag, postfix=postfix)
	return False
