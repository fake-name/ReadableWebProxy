def extractMaynoveltranslationsCom(item):
	'''
	Parser for 'maynoveltranslations.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('president shen always top up money',       'president shen always top up money',                      'translated'),
		('Rebirth of Brotherly Love',                'Rebirth of Brotherly Love',                               'translated'),
		('Rebirth of Chen An',                       'Rebirth of Chen An',                                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False