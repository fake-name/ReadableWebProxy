def extractDistractedTranslations(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	ltags = [tmp.lower() for tmp in item['tags']]
	if 'gonna get captured' in ltags or 'Get Captured: Chapter' in item['title']:
		return buildReleaseMessageWithType(item, 'Like Hell I’m Gonna Get Captured!', vol, chp, frag=frag, postfix=postfix)
	if 'Girl Who Ate Death' in item['title']:
		return buildReleaseMessageWithType(item, 'Shinigami wo Tabeta Shouko', vol, chp, frag=frag, postfix=postfix)
	return False
