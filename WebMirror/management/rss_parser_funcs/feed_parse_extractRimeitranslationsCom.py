def extractRimeitranslationsCom(item):
	'''
	Parser for 'rimeitranslations.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('evil wang pampers his ghost doctor fei',       'evil wang pampers his ghost doctor fei',                      'translated'),
		('general you have it',               'general you have it',                              'translated'),
		('paper plane',                       'paper plane',                                      'translated'),
		('rebirth plan to save leader',       'rebirth plan to save leader',                      'translated'),
		('general, you have it',              'general, you have it',                             'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False