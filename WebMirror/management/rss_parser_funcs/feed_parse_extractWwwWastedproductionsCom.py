def extractWwwWastedproductionsCom(item):
	'''
	Parser for 'www.wastedproductions.com'
	'''
	
	badwords = [
			'#ninerwrimo',
			'#NaNoWriMo',
			'#ThursdayTales',
			'#StoryCubes',
		]
	if any([bad in item['tags'] for bad in badwords]):
		return None



	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('PRC',       'PRC',                      'translated'),
		('Hollow World', 'Hollow World',                'oel'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False