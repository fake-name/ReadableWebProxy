def extractSilentTl(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	
	if 'Legend' in item['tags']:
		return buildReleaseMessageWithType(item, 'Legend', vol, chp, frag=frag, postfix=postfix)
		
	tagmap = [
		('cafe',         'The Dutch Slope’s Western Cafe',                      'translated'),
		('Legend',       'Legend',                                              'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
	return False