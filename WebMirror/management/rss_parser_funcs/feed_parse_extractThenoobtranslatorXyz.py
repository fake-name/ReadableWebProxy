def extractThenoobtranslatorXyz(item):
	'''
	Parser for 'thenoobtranslator.xyz'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
		
	if item['tags'] == ['Uncategorized']:
	
		titlemap = [
			('PS Chapter ',    'Perfect Superstar',               'translated'),
			('HDLL Chapter ',  'House Dad\'s Literary Life',      'translated'),
		]
	
		for titlecomponent, name, tl_type in titlemap:
			if titlecomponent.lower() in item['title'].lower():
				return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)
	

	tagmap = [
			('Perfect Superstar',           'Perfect Superstar',               'translated'),
			('House Dad\'s Literary Life',  'House Dad\'s Literary Life',      'translated'),
			('House Dad Literary Life',     'House Dad\'s Literary Life',      'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False