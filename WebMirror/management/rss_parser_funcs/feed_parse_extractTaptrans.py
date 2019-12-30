def extractTaptrans(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Manga' in item['tags']:
		return None
	if 'Doujinshi' in item['tags']:
		return None
		
	return False