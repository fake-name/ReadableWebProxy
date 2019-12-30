def extractWhiteskytranslationsWordpressCom(item):
	'''
	Parser for 'whiteskytranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('A Wave of Exes',       'A Wave of Exes',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	if item['tags'] != ['Uncategorized']:
		return False
		
	chp_prefixes = [
			('Quickly Wear the Face of the Devil',              'Quickly Wear the Face of the Devil',                             'translated'),
			('Rebirth of a Movie Star',                         'Rebirth of a Movie Star',                                        'translated'),
			('A Wave of Exes',                                  'A Wave of Exes',                                                 'translated'),
			('The Scum Shou’s Survival Guide – Chapter ',       'The Scum Shou\'s Survival Guide',                                'translated'),
		]

	for prefix, series, tl_type in chp_prefixes:
		if item['title'].lower().startswith(prefix.lower()):
			return buildReleaseMessageWithType(item, series, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False