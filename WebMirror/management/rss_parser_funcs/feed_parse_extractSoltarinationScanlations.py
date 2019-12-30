def extractSoltarinationScanlations(item):
	"""
	# 'Soltarination Scanlations'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	if 'Light Novels' not in item['tags']:
		return None
	
	if 'Light Novel Summaries' in item['tags']:
		return None
		
	return False