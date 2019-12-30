def extractMiumiuSMusings(item):
	"""
	Parser for 'Miumiu's musings'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None

	tagmap = [
		('iydgth',               'If You Don’t Go To Hell, Who Will? ',        'translated'),
		('NCND',                 'Nuptial Chamber Next Door',                  'translated'),
		('Rolling Love',         'Rolling Love',                               'translated'),
		('Same bed',             'Same Place Not Same Bed',                    'translated'),
		('Nuptial Chamber',      'Nuptial Chamber Next Door',                  'translated'),
		('Love You',             'Loving You Is Too difficult',                'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		

	if item['tags'] != ['Uncategorized']:
		return False
		
		
	chp_prefixes = [
			('NCND – ',                            'Nuptial Chamber Next Door',                 'translated'),
			('NCND – ',                            'Nuptial Chamber Next Door',                 'translated'),
			('Loving You Is Too difficult – ',     'Loving You Is Too difficult',               'translated'),
		]

	for prefix, series, tl_type in chp_prefixes:
		if item['title'].lower().startswith(prefix.lower()):
			return buildReleaseMessageWithType(item, series, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
	return False