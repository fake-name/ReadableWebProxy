def extractTheSunIsColdTranslations(item):
	"""
	Parser for 'The Sun Is Cold Translations'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if '108 maidens' in item['tags']:
		return buildReleaseMessageWithType(item, '108 Maidens of Destiny', vol, chp, frag=frag, postfix=postfix)
	if 'Back to the Apocalypse' in item['tags']:
		return buildReleaseMessageWithType(item, 'Back to the Apocalypse', vol, chp, frag=frag, postfix=postfix)
	return False
