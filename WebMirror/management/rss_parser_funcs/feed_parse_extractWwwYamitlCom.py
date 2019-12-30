def extractWwwYamitlCom(item):
	'''
	Parser for 'www.yamitl.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Illimitable Until Death',       'Illimitable Until Death',                      'translated'),
		('Summoner of Miracles',          'Summoner of Miracles',                         'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False