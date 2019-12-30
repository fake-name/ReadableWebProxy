def extractTranslatingForYourPleasure(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if "The Inverted Dragon's Scale" in item['tags']:
		return buildReleaseMessageWithType(item, "The Inverted Dragon's Scale", vol, chp, frag=frag, postfix=postfix)
	return False
