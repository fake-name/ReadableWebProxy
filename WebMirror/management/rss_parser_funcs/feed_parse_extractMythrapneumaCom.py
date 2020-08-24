def extractMythrapneumaCom(item):
	'''
	Parser for 'mythrapneuma.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('infinite apostle and twelve war maidens',       'infinite apostle and twelve war maidens',                      'translated'),
		('infinite apostle and twelve war girls',       'infinite apostle and twelve war maidens',                      'translated'),
		('unlimited apostle and twelve war maidens',       'infinite apostle and twelve war maidens',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False