def extractLittleNovelTranslation(item):
	"""
	# 'Little Novel Translation'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'GTI Release' in item['tags']:
		return buildReleaseMessageWithType(item, 'Godly Thief Incarnation', vol, chp, frag=frag, postfix=postfix)
	return False
