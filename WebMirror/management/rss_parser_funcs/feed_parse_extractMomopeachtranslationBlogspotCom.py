def extractMomopeachtranslationBlogspotCom(item):
	'''
	Parser for 'momopeachtranslation.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Billion of Pampering Only For You',                 'Billion of Pampering Only For You',                                'translated'),
		('Beloved Wife on Top : Master Mo Softly Kiss',       'Beloved Wife on Top : Master Mo Softly Kiss',                      'translated'),
		('Wealthy Family\'s Warm Wedding',                    'Wealthy Family\'s Warm Wedding',                                   'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False