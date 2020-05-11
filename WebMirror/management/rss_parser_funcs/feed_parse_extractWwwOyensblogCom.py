def extractWwwOyensblogCom(item):
	'''
	Parser for 'www.oyensblog.com'
	'''


	badwords = [
			'Diary',
		]
	if any([bad in item['tags'] for bad in badwords]):
		return None



	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('the king\'s return',                    'The King\'s Return',                      'translated'),
		('She Become Sweet and Cuddly',       'She Become Sweet and Cuddly',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	titlemap = [
		('The Anarchic Consort : Chapter ',         'The Anarchic Consort',      'translated'),
		('She Become Sweet and Cuddly : Chapter ',  'She Become Sweet and Cuddly',      'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False