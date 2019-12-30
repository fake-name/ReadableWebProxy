def extractIsekaiTranslation(item):
	"""
	# Isekai Soul-Cyborg Translations

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Manga' in item['tags']:
		return None
		
	if 'Isekai Maou to Shoukan Shoujo Dorei Majutsu' in item['tags'] and (chp or vol) and not 'manga' in item['title'].lower():
		if chp == 11 and frag == 10:
			return None
		return buildReleaseMessageWithType(item, 'Isekai Maou to Shoukan Shoujo no Dorei Majutsu', vol, chp, frag=frag, postfix=postfix)
	return False