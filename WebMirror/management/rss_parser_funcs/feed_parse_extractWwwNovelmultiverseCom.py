def extractWwwNovelmultiverseCom(item):
	'''
	Parser for 'www.novelmultiverse.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('elememtaryharem',                                         'After returning to elementary school with my memory the result was to create a harem',   'translated'),
		('elementaryharem',                                         'After returning to elementary school with my memory the result was to create a harem',   'translated'),
		('Parameter remote controller',                             'Parameter remote controller',                                                            'translated'),
		('auto assigned villainess',                                'auto assigned villainess',                                                               'translated'),
		('the reincarnated young lady aims to be an adventurer',    'the reincarnated young lady aims to be an adventurer',                                   'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False