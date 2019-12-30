def extractAinushiTranslations愛主の翻訳(item):
	"""
	Ainushi Translations 愛主の翻訳
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	return False
