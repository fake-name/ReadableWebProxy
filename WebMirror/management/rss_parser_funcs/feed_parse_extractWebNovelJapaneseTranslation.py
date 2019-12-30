def extractWebNovelJapaneseTranslation(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Kizoku Yamemasu Shomin ni Narimasu' in item['tags']:
		return buildReleaseMessageWithType(item, 'Kizoku Yamemasu Shomin ni Narimasu', vol, chp, frag=frag, postfix=postfix)
	return False
