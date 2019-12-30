def extractNanjamora(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Endless Dantian' in item['tags']:
		return buildReleaseMessageWithType(item, 'Endless Dantian', vol, chp, frag=frag, postfix=postfix)
	if 'Infinite Temptation' in item['tags']:
		return buildReleaseMessageWithType(item, 'Infinite Temptation', vol, chp, frag=frag, postfix=postfix)
	if 'wushang jinshia' in item['tags']:
		return buildReleaseMessageWithType(item, 'Wu Shang Jin Shia', vol, chp, frag=frag, postfix=postfix)
	return False
