def extractPeachpittingCom(item):
	'''
	Parser for 'peachpitting.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('There Will Always Be Protagonists With Delusions of Starting a Harem',       'There Will Always Be Protagonists With Delusions of Starting a Harem',                      'translated'),
		('i have a pair of yin-yuan eyes',       'i have a pair of yin-yuan eyes',                      'translated'),
		('My Cherry Will Explode in the Apocalypse',       'My Cherry Will Explode in the Apocalypse',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False