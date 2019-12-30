def extractWhateverTranslationsMTL(item):
	"""
	Whatever Translations MTL
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	if item['title'].lower().startswith('level maker ch'):
		return buildReleaseMessageWithType(item, 'Level Maker', vol, chp, frag=frag, postfix=postfix)
	if item['title'].lower().startswith('levelmaker ch'):
		return buildReleaseMessageWithType(item, 'Level Maker', vol, chp, frag=frag, postfix=postfix)
		
	return False