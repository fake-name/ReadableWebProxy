def extractLnreadsCom(item):
	'''
	Parser for 'lnreads.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('My Amazing WeChat',                             'My Amazing WeChat',                                                            'translated'),
		('special agent’s rebirth',                       'Special Agent’s Rebirth: The Almighty Goddess of Quick Transmigration',        'translated'),
		('the almighty martial arts system',              'the almighty martial arts system',                                             'translated'),
		('returning after 10000 years cultivation',       'returning after 10000 years cultivation',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False