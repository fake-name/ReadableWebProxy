def extractAkaitranslatesWordpressCom(item):
	'''
	Parser for 'akaitranslates.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('The Duke\'s Daughter is the Knight Captain\'s (62) Young Wife',       'The Duke\'s Daughter is the Knight Captain\'s (62) Young Wife',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]
	
	if 'The Duke\'s Daughter is the Knight Captain\'s (62) Young Wife' in item['tags'] and chp == 62:
		return None
		
	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False