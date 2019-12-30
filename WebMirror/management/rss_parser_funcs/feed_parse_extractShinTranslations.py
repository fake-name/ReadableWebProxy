def extractShinTranslations(item):
	"""
	# Shin Translations

	"""
	
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
		
	if 'THE NEW GATE' in item['tags'] and not 'Status Update' in item['tags']:
		
		return buildReleaseMessageWithType(item, 'The New Gate', vol, chp, frag=frag)
		
	return False