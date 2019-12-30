def extractPaztok(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title']:
		return False
	if not postfix and ':' in item['title']:
		postfix = item['title'].split(':')[-1]
	if 'Paztok' in item['tags']:
		return buildReleaseMessageWithType(item, 'Paztok', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False
