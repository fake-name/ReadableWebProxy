def extractDarkTranslations(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if item['title'].lower().startswith('kuang shen'):
		return buildReleaseMessageWithType(item, 'Kuang Shen', vol, chp, frag=frag, postfix=postfix)
	if item['title'].lower().startswith('sheng wang chapter'):
		return buildReleaseMessageWithType(item, 'Sheng Wang', vol, chp, frag=frag, postfix=postfix)
	if 'lord xue ying chapter' in item['title'].lower():
		return buildReleaseMessageWithType(item, 'Lord Xue Ying', vol, chp, frag=frag, postfix=postfix)
	return False
