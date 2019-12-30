def extractBirdyTranslations(item):
	"""
	Parser for 'Birdy Translations'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if item['title'].startswith('Spear Master and the Black Cat Chapter '):
		return buildReleaseMessageWithType(item, 'Spear Master and the Black Cat', vol, chp, frag=frag, postfix=postfix)
	return False
