def extractTranslatorEri(item):
	"""
	Parser for 'Translator Eri'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if "asks" in item['tags']:
		return None
	if "replied to your&nbsp;post: " in item['title']:
		return None
		
	if 'WATTT' in item['tags']:
		return buildReleaseMessageWithType(item, 'WATTT', vol, chp, frag=frag, postfix=postfix)
	return False