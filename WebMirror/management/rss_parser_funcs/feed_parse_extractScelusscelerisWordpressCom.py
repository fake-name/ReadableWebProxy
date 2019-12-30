def extractScelusscelerisWordpressCom(item):
	'''
	Parser for 'scelussceleris.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Tensei Shite Inaka de Slowlife wo Okuritai',       'Tensei Shite Inaka de Slowlife wo Okuritai',                      'translated'),
		('tensei shite inaka',                               'Tensei Shite Inaka de Slowlife wo Okuritai',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False