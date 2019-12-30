def extractTurtleandHareTranslations(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Time (对的时间对的人)' in item['title'] or 'Time (对的时间对的人)' in item['tags']:
		return buildReleaseMessageWithType(item, 'Time', vol, chp, frag=frag, postfix=postfix)
	return False
