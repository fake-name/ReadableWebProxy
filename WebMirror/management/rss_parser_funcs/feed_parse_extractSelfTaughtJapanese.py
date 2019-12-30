def extractSelfTaughtJapanese(item):
	"""
	Self Taught Japanese
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'travel' in item['tags']:
		return None
	if 'Japanese Study: Advanced' in item['tags']:
		return None
	if 'contests' in item['tags']:
		return None
	if 'test' in item['tags']:
		return None
	if 'grammar' in item['tags']:
		return None
	if 'research' in item['tags']:
		return None
	if 'Reviews' in item['tags']:
		return None
	if 'aside' in item['tags']:
		return None
		
		
	return False