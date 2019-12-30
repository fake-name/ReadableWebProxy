def extractKnightFantasticNightTranslations(item):
	"""
	Knight Fantastic Night Translations
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'RAW' in item['title']:
		return False
	if 'Knight Fantastic Night' in item['tags']:
		return buildReleaseMessageWithType(item, 'Knight Fantastic Night', vol, chp, frag=frag, postfix=postfix)
	if 'The Bride of The Serpent Prince' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Bride of The Serpent Prince', vol, chp, frag=frag, postfix=postfix)
	return False
