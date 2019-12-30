def extractSlothTranslationsBlog(item):
	"""
	# 'Sloth Translations Blog'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if item['title'].startswith('Re:Master Magic '):
		return buildReleaseMessageWithType(item, 'The Mage Will Master Magic Efficiently In His Second Life', vol, chp, frag=frag, postfix=postfix)
	if item['title'].lower().startswith('blacksmith chapter '):
		return buildReleaseMessageWithType(item, 'Botsuraku youtei nanode, Kajishokunin wo mezasu', vol, chp, frag=frag, postfix=postfix)
	if item['title'].lower().startswith('evil lord'):
		return buildReleaseMessageWithType(item, 'I’m the Evil Lord of an Intergalactic Empire!', vol, chp, frag=frag, postfix=postfix)
		
		
		
	return False