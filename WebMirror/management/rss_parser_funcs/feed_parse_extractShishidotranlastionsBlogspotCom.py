def extractShishidotranlastionsBlogspotCom(item):
	'''
	Parser for 'shishidotranlastions.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('i’m troubled by the prince’s love ~ reincarnated heroine~the otome game struggle',       'i’m troubled by the prince’s love ~ reincarnated heroine~the otome game struggle',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False