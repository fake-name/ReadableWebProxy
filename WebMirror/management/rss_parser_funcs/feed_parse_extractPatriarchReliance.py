def extractPatriarchReliance(item):
	"""
	# 'Patriarch Reliance'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if re.match('Chapters? \\d+', item['title']):
		return buildReleaseMessageWithType(item, 'God and Devil World', vol, chp, frag=frag, postfix=postfix)
	return False
