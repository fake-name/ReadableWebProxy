def extractPlantTranslation(item):
	"""
	'Plant Translation'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	tagmap = [
		('cultutral inavsion in different world',          'cultutral inavsion in different world',    'translated'),
		('Heavenly Farmer',                                'Heavenly Farmer',                          'translated'),
		('The Strongest Gene',                             'The Strongest Gene',                       'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)
			
	return False