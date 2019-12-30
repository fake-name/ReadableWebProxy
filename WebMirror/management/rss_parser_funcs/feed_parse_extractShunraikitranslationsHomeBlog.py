def extractShunraikitranslationsHomeBlog(item):
	'''
	Parser for 'shunraikitranslations.home.blog'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Positive Energy System',          'Positive Energy System',                         'translated'),
		('PES',                             'Positive Energy System',                         'translated'),
		('More Than A Few Blessings',       'More Than A Few Blessings',                      'translated'),
		('MTaFB',                           'More Than A Few Blessings',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False