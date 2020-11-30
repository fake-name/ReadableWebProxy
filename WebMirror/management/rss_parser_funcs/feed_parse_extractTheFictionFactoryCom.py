def extractTheFictionFactoryCom(item):
	'''
	Parser for 'the-fiction-factory.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('monster no goshujin-sama',             'monster no goshujin-sama',                            'translated'),
		('ossan bouken-sha kein no zenko',       'ossan bouken-sha kein no zenko',                      'translated'),
		('tatoeba ore ga',                       'tatoeba ore ga',                                      'translated'),
		('dorei tensei',                         'dorei tensei',                                        'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False