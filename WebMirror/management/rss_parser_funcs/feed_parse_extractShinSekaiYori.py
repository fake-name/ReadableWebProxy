def extractShinSekaiYori(item):
	"""

	"""
	chStr = ''
	for tag in item['tags']:
		if 'chapter' in tag.lower():
			chStr = chStr + ' ' + tag
	chStr += ' ' + item['title']
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(chStr)
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if frag:
		frag = frag / 10
	return buildReleaseMessageWithType(item, 'Shin Sekai yori', vol, chp, frag=frag, postfix=postfix)
