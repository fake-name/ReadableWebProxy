def extractFudgeTranslations(item):
	"""
	# Fudge Translations

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'SoE' in item['title'] and (chp or vol):
		return buildReleaseMessageWithType(item, 'The Sword of Emperor', vol, chp, frag=frag, postfix=postfix)
	if item['title'].startswith('Emperor of Solo Play Chapter') and (chp or vol):
		return buildReleaseMessageWithType(item, 'Emperor of Solo Play', vol, chp, frag=frag, postfix=postfix)
	return False
