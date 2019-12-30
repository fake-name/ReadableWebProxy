def extractWanderingmusetranslationWordpressCom(item):
	'''
	Parser for 'wanderingmusetranslation.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	chp_prefixes = [
			('SH Chapter ',  'Swain Hakushaku',                                                                      'translated'),
			('AS Chapter ',  'My Status As An Assassin Is Obviously Stronger Than That Of the Hero’s',               'translated'),
			('Cat ',    'Me and My Beloved Cat (Girlfriend)',                                  'translated'),
		]
	
	if item['tags'] == ['Uncategorized']:
		for prefix, series, tl_type in chp_prefixes:
			if item['title'].lower().startswith(prefix.lower()):
				return buildReleaseMessageWithType(item, series, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



	tagmap = [
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False