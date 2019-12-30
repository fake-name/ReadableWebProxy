def extractSofluffytranslationsCom(item):
	'''
	Parser for 'sofluffytranslations.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Italian First Love Diary',       'An Italian first love diary',                      'translated'), 
		('Good Morning Miss Ghost',        'Good Morning Miss Ghost',                          'translated'), 
		('Good Morning Miss Ghost',          'Good Morning Miss Ghost',                         'translated'),
		('Evil Husband, Don\'t Tease',       'Evil Husband, Don\'t Tease',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False