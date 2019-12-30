def extractWwwCookienovelsCom(item):
	'''
	Parser for 'www.cookienovels.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('female-general-and-eldest-princess',                   'Female General And Eldest Princess',                                  'translated'),
		('facing-you',                                           'Facing You',                                                          'translated'),
		('the weakest tamer trash picking journey begins',       'the weakest tamer trash picking journey begins',                      'translated'),
		('can i become an adventurer without gift?',             'can i become an adventurer without gift?',                            'translated'),
		('can i become an adventurer without gifts?',            'can i become an adventurer without gift?',                            'translated'),
		('ex-brave wants a quiet life',                          'ex-brave wants a quiet life',                                         'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False