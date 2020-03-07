def extractElegantgoddesstranslationWordpressCom(item):
	'''
	Parser for 'elegantgoddesstranslation.wordpress.com'
	'''
	
	
	badwords = [
			'quotes',
			'youtube',
			'Music',
			'badword',
		]
	if any([bad in item['tags'] for bad in badwords]):
		return None



	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('the white-haired imperial consort',       'The White-Haired Imperial Concubine',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False