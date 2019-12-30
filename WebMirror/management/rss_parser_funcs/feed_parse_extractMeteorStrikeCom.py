def extractMeteorStrikeCom(item):
	'''
	Parser for 'meteor-strike.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('PRC',       'PRC',                                            'translated'),
		('WGM',       'World\'s Greatest Militia',                      'translated'),
		('re;s',      'RE: Survival',                                   'translated'),
		('FM',        'Fallen Monarch',                                 'translated'),
		('Loiterous', 'Loiterous',                                      'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False