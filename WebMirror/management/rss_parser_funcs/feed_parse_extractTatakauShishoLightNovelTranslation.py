def extractTatakauShishoLightNovelTranslation(item):
	"""

	"""
	
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(str(item['tags']) + item['title'])
	if not (chp or frag) or 'preview' in item['title'].lower():
		return None
	
	if not any(['volume' in tag.lower() for tag in item['tags']]):
		return None
	
	if item['title'].startswith("Chapter "):
		return buildReleaseMessageWithType(item, 'Tatakau Shisho', vol, chp, frag=frag, postfix=postfix)
		
	return False