def extractMonkotosTranslations(item):
	"""
	# "Monkoto's Translations"
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Chapter Release' in item['tags'] and 'Ryuugoroshi' in item['title']:
		return buildReleaseMessageWithType(item, 'Ryugoroshi no Sugosuhibi', vol, chp, frag=frag, postfix=postfix)
	return False
