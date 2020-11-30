def extractAmnesiactlCom(item):
	'''
	Parser for 'amnesiactl.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('i\'ll never go back to bygone days!',       'I\'ll never go back to bygone days!',                      'translated'),
		('banished failure',                          'banished failure',                                         'translated'),
		('tokyo survive',                             'tokyo survive',                                            'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False