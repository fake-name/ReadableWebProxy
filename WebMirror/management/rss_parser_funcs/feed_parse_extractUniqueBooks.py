def extractUniqueBooks(item):
	"""
	Unique Books
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Allgemein' in item['tags']:
		return buildReleaseMessageWithType(item, 'Survival of a Healer', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False
