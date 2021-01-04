def extractLyletranslatesWordpressCom(item):
	'''
	Parser for 'lyletranslates.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('PRC',       'PRC',                      'translated'),
		('i found a husband when i picked up the male lead', 'I Found a Husband When I Picked up the Male Lead',                'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]
	
	if 'original work' in item['tags']:
		return False
	
	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False