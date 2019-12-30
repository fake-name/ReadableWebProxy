def extractLypheonMachineTranslation(item):
	"""
	# 'Lypheon Machine Translation'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	return False
