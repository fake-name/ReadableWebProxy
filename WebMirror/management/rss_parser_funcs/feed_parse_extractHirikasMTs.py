def extractHirikasMTs(item):
	"""
	"Hirika's MTs"
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	tagmap = {
		'IDWTDIAOG'                                  : 'I Don\'t Want To Die In An Otome Game',
		'SBS'                                        : 'Sleeping Beauty\'s Sweets',
	}

	for tag, sname in tagmap.items():
		if tag in item['tags']:
			return buildReleaseMessageWithType(item, sname, vol, chp, frag=frag)
			
	return False