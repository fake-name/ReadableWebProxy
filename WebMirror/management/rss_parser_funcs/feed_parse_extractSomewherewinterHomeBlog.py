def extractSomewherewinterHomeBlog(item):
	'''
	Parser for 'somewherewinter.home.blog'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Who Dares Slander My Senior Brother',       'Who Dares Slander My Senior Brother',                      'translated'),
		('Thousand Autumns',                          'Thousand Autumns',                                         'translated'),
		('Sweet Heart in Honeyed Desire',             'Sweet Heart in Honeyed Desire',                            'translated'),
		('Xian Wang Dotes On Wife',                   'Xian Wang Dotes On Wife',                                  'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False