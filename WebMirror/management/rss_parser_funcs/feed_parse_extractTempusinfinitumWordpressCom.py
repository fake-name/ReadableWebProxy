def extractTempusinfinitumWordpressCom(item):
	'''
	Parser for 'tempusinfinitum.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Ultimate Porter',       'Ultimate Porter ~The weakest man aspires to be an adventurer~',                      'translated'),
		('Maou Gakuin No Futekigousha',       'Maou Gakuin No Futekigousha',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False