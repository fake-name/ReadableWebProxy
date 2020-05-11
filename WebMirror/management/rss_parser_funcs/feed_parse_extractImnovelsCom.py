def extractImnovelsCom(item):
	'''
	Parser for 'imnovels.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('idtml',        'I Dumped the Male Lead Before an Apocalypse',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('iterum incipi', 'Iterum Incipi',                'oel'),
		('tbab',          'To Be a Beauty',                'oel'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False