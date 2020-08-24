def extractLilistranslationsWordpressCom(item):
	'''
	Parser for 'lilistranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('little expert bending plot lines back',       'Little Expert Bending Plot Lines Back (Quick Transmigration)',                      'translated'),
		('i\'m afraid i\'m now a salted fish',          'I’m Afraid I’m Now a Salted Fish (Entertainment Circle)',                      'translated'),
		('i\'m afraid it\'s a salted fish',          'I’m Afraid I’m Now a Salted Fish (Entertainment Circle)',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False