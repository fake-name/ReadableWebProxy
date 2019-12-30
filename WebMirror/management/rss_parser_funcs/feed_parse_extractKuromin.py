def extractKuromin(item):
	"""
	Kuromin
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if item['title'].startswith('Potatoes are the only thing that’s needed in this world! Chapter'):
		return buildReleaseMessageWithType(item, 'Potatoes are the only thing that’s needed in this world!', vol, chp, frag=frag, postfix=postfix)
	return False
