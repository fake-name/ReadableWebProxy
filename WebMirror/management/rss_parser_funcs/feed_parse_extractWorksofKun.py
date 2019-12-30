def extractWorksofKun(item):
	"""
	'Works of Kun'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Apocalypse Cockroach' in item['tags']:
		return buildReleaseMessageWithType(item, 'Apocalypse Cockroach', vol, chp, frag=frag, postfix=postfix)
	return False
