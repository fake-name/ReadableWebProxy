def extractWorkingNEETTranslation(item):
	"""
	'Working NEET Translation'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	
	if "Translation progress" in item['tags']:
		return None
	if 'Announcement' in item['tags']:
		return None
		
	tagmap = {
		'Dark Magician as a Hero'                                   : 'Dark Magician as a Hero',
		'Izure Shinwa no Ragnarok'                                  : 'Izure Shinwa no Ragnarok',
		'NEET Hello Work'                                           : 'I’m a NEET but when I went to Hello Work I got taken to another world',
	}
	

	for tag, sname in tagmap.items():
		if tag in item['tags']:
			return buildReleaseMessageWithType(item, sname, vol, chp, frag=frag)
	
	
	if item['tags'] == ['Volume 4'] or item['tags'] == ['Volume 3']:
		return buildReleaseMessageWithType(item, 'I’m a NEET but when I went to Hello Work I got taken to another world', vol, chp, frag=frag)
	
	
	return False