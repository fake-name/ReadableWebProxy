def extractChichilationsHomeBlog(item):
	'''
	Parser for 'chichilations.home.blog'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Qinglian Chronicles',       'Qinglian Chronicles',                      'translated'),
		('dkgwf',                     'Didn\'t Know General Was Female',          'translated'),
		('Golden Stage',              'Golden Stage',                             'translated'),
		('eastward flow',             'Eastward Flow',                            'translated'),
		('Lord Seventh',              'Lord Seventh',                             'translated'),
		('dragon drowned',            'dragon drowned',                           'translated'),
		('beauty and the blade',      'beauty and the blade',                     'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False