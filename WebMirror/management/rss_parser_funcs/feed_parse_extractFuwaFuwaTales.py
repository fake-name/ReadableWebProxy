def extractFuwaFuwaTales(item):
	"""
	Fuwa Fuwa Tales
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	tagmap = [
		('Prince Herscherik and The Kingdom of Sorrow',                 'Prince Herscherik and The Kingdom of Sorrow',                                'translated'),
		('By A Slight Mistake',                                         'By A Slight Mistake',                                                        'translated'),
		('The Magnificent Battle Records of a Former Noble Lady',       'The Magnificent Battle Records of a Former Noble Lady',                      'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



	return False