def extractPadamtlWordpressCom(item):
	'''
	Parser for 'padamtl.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('PBD',                      'Peach Blossom Debt',                                                                        'translated'),
		('Peach Blossom Debt',       'Peach Blossom Debt',                                                                        'translated'),
		('APDSH',                    'There Will Always Be Protagonists With Delusions of Starting a Harem',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False