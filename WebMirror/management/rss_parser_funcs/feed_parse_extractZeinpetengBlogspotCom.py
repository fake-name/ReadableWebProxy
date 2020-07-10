def extractZeinpetengBlogspotCom(item):
	'''
	Parser for 'zeinpeteng.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('the escape of layla',       'the escape of layla',                      'translated'),
		('jimi de medatanai watashi wa kyou de owari ni shimasu',       'jimi de medatanai watashi wa kyou de owari ni shimasu',                      'translated'),
		('hariko no otome',       'hariko no otome',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False