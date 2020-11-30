def extractVouriatransBlogspotCom(item):
	'''
	Parser for 'vouriatrans.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('ibtmlff',       'I Became The Male Lead\'s Female Friend.',                      'translated'),
		('irvp',          'I Raised the Villains Preciously',                      'translated'),
		('tinpff',        'There is No Place For Fakes',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False