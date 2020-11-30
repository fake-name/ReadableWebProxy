def extractHobbycuresboredomBlogspotCom(item):
	'''
	Parser for 'hobbycuresboredom.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('crc',       'Cultivator Returns to the City',                      'translated'),
		('lawmm',      'Life in Another World as a Maid Mage',                      'translated'),
		('eue',       'Era of Universal Evolution',                      'translated'),
		('IHASH',      'I Have A \'System\' Halo',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False