def extractBbmtlsWordpressCom(item):
	'''
	Parser for 'bbmtls.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('RBDLS',                                        'Raising a Bun with a Daily Life System',                      'translated'),
		('Raising a Bun with a Daily Life System',       'Raising a Bun with a Daily Life System',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False