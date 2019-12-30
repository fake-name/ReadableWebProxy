def extractPiggyBottleTranslations(item):
	"""
	#'PiggyBottle Translations'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if item['title'].lower().startswith('beseech the devil'):
		return buildReleaseMessageWithType(item, 'Beseech the Devil', vol, chp, frag=frag, postfix=postfix)
	return False
