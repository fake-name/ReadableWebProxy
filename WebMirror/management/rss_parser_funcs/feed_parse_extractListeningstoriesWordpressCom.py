def extractListeningstoriesWordpressCom(item):
	'''
	Parser for 'listeningstories.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Okoborehime to Entaku no Kishi',       'Okoborehime to Entaku no Kishi',                      'translated'),
		('okoborehime',                          'Okoborehime to Entaku no Kishi',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False