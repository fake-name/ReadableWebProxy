def extractRenaNSekaiBlogspotCom(item):
	'''
	Parser for 'rena-n-sekai.blogspot.com'
	'''


	badwords = [
			'drama CD',
			'character song',
			'Doujin',
			'badword',
		]
	if any([bad in item['tags'] for bad in badwords]):
		return None




	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('i don\'t want to die in an otome game',       'i don\'t want to die in an otome game',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False