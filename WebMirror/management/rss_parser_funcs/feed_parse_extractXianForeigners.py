def extractXianForeigners(item):
	"""
	'Xian Foreigners'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'President Wife Is A Man' in item['tags']:
		return buildReleaseMessageWithType(item, 'President Wife Is A Man', vol, chp, frag=frag, postfix=postfix)
	return False
