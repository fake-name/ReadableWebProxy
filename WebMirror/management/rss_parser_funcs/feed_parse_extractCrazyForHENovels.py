def extractCrazyForHENovels(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) and not 'preview' in item['title']:
		return False
	chp = frag
	frag = None
	if '如果蜗牛有爱情 When A Snail Loves – 丁墨 Ding Mo (HE)(Incomplete)' in item['tags'] or 'When a snail loves' in item['tags']:
		return buildReleaseMessageWithType(item, 'When A Snail Loves', vol, chp, frag=frag, postfix=postfix)
	return False
