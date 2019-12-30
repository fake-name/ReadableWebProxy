def extractOneManArmy(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'DBWG – Chapter' in item['title'] or 'Dragon-Blooded War God' in item['tags']:
		return buildReleaseMessageWithType(item, 'Dragon-Blooded War God', vol, chp, frag=frag, postfix=postfix)
	if 'Warlock of the Magus World' in item['tags']:
		return buildReleaseMessageWithType(item, 'Warlock of the Magus World', vol, chp, frag=frag, postfix=postfix)
	return False
