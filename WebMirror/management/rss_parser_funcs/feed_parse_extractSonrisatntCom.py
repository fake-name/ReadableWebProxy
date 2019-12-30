def extractSonrisatntCom(item):
	'''
	Parser for 'sonrisatnt.com'
	'''


	badwords = [
			'C-Drama',
		]
	if any([bad in item['tags'] for bad in badwords]):
		return None



	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Ostentatious Zhao Yao',       'Ostentatious Zhao Yao',                      'translated'),
		('100 Ghost Collection',        '100 Ghost Collection',                       'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False