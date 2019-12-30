def extractNextlevelforthePLOT(item):
	"""
	'Next level for the PLOT'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp is not None or vol is not None or frag is not None) or 'preview' in item['title'].lower():
		return None
		
	if 'scan-trad' in item['tags']:
		return None
		
	tagmap = [
		('Ore Ga Heroine',       'Ore ga Heroine wo Tasukesugite Sekai ga Little Mushiroku',                      'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
		
	titlemap = [
		('For my daughter, I might defeat even the archenemy Chapter',  'For my daughter, I might defeat even the archenemy',      'translated'), 
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
	return False