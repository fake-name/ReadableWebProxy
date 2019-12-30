def extractBLNovelObsession(item):
	"""
	'BL Novel Obsession'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	if 'Feng Mang' in item['tags']:
		return buildReleaseMessageWithType(item, 'Feng Mang', vol, chp, frag=frag, postfix=postfix)
		
	
	tagmap = [
		('Deceive',          'Deceive',                        'translated'),
		('Feng Mang',        'Feng Mang',                      'translated'),
		('15P 7H 6SM',       '15P 7H 6SM',                     'translated'),
		('goldenassistant',  'Golden Assistant',               'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
	return False