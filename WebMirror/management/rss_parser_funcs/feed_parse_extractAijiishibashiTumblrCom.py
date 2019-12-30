def extractAijiishibashiTumblrCom(item):
	'''
	Parser for 'aijiishibashi.tumblr.com'
	'''
	
	bad = [
			'ask',
			'kochou no yumeji',
			'isekai omotenashi gohan',
		]
	
	if any([tmp in item['tags'] for tmp in bad]):
		return None
	
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('PRC',       'PRC',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False