def extractTheBoyWhoCouldntBeAHero(item):
	"""
	The Boy Who Couldn't Be A Hero
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	return False
