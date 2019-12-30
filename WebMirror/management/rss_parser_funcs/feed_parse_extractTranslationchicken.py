def extractTranslationchicken(item):
	"""
	Parser for 'TranslationChicken'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 're:zero' in item['tags']:
		return buildReleaseMessageWithType(item, 'Re:Zero Kara Hajimeru Isekai Seikatsu (WN)', vol, chp, frag=frag, postfix=postfix)
	return False