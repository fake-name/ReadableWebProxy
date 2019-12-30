def extractSuikodenISoulEaterNovelTranslation(item):
	"""
	Parser for 'Suikoden I: Soul Eater Novel Translation'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
		
	if 'Soul Eater' in item['tags']:
		return buildReleaseMessageWithType(item, 'Soul Eater', vol, chp, frag=frag, postfix=postfix)
		
	return False