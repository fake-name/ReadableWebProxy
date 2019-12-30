def extractEmeraldmayblossomBlogspotCom(item):
	'''
	Parser for 'emeraldmayblossom.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('I Heard You Like Me Too (聽說你也喜歡我)',                    'I Heard You Like Me Too',                                 'translated'),
		('Precisely In Love With You (就是愛上你)',                     'Precisely In Love With You',                              'translated'),
		('i want to waste away time with you (我想和你互相浪費)',       'I want to waste away time with you',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False