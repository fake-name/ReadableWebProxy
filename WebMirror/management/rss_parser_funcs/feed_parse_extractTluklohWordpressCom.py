def extractTluklohWordpressCom(item):
	'''
	Parser for 'tlukloh.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('elementaryharem',       'After returning to elementary school with my memory the result was to create a harem',                      'translated'),
		('elememtaryharem',       'After returning to elementary school with my memory the result was to create a harem',                      'translated'),
		('PRC',       'After returning to elementary school with my memory the result was to create a harem',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False