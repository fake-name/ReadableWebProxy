def extractLovelyxDay(item):
	"""
	'Lovely x Day'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'WSU' in item['tags']:
		return buildReleaseMessageWithType(item, "Because I'm a Weapon Shop Uncle", vol, chp, frag=frag, postfix=postfix)
	return False
