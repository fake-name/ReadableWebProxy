def extractDreamsintheseaTumblrCom(item):
	'''
	Parser for 'dreamsinthesea.tumblr.com'
	'''
	
	
	badwords = [
			'fashion',
			'pokemon',
			'tessa thompson',
		]
	if any([bad in item['tags'] for bad in badwords]):
		return None



	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('the s ranks that i\'ve raised',       'The S-Ranks that I\'ve raised',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False