def extractSelfTaughtJapanese(item):
	"""
	Self Taught Japanese
	"""
	

	badwords = [
			'travel',
			'Japanese Study: Intermediate',
			'Japanese Study: Advanced',
			'contests',
			'E-book publishing',
			'test',
			'grammar',
			'research',
			'Reviews',
			'aside'
			
		]
	if any([bad in item['tags'] for bad in badwords]):
		return None


	
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None

		
	return False