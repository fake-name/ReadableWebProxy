def extractBeerHappyTranslations(item):
	"""
	Parser for 'Beer Happy Translations'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
		
	if "Shaman's Awakening" in item['tags']:
		return buildReleaseMessageWithType(item, "Shaman's Awakening", vol, chp, frag=frag, postfix=postfix)
		
	return False