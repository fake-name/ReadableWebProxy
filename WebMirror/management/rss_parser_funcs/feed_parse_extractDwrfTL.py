def extractDwrfTL(item):
	"""
	Dwrf TL
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	tagmap = [
		('the world is fun as it became a death game',       'The World Has Become a Death Game and It\'s Fun',                      'translated'),
		('DG:FW',                                            'The World Has Become a Death Game and It\'s Fun',                      'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	return False