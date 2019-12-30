def extractMagustranslationsWordpressCom(item):
	'''
	Parser for 'magustranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	if item['tags'] == ['Uncategorized'] and item['title'].startswith("Chapter "):
		return buildReleaseMessageWithType(item, 'Light Spirit Epic', vol, chp, frag=frag, postfix=postfix, tl_type='translated')
		
	tagmap = [
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	

	
	return False