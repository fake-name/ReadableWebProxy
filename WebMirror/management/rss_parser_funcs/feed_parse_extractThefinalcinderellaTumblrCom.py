def extractThefinalcinderellaTumblrCom(item):
	'''
	Parser for 'thefinalcinderella.tumblr.com'
	'''


	badwords = [
			'tsurune dvd translations',
			'a3! anime',
			'twisted wonderland spoilers',
			'pjo',
			'ask',
			'badword',
		]
	if any([bad in item['tags'] for bad in badwords]):
		return None



	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('tsurune',                        'Tsurune: Kazemai Koukou Kyuudoubu',             'translated'),
		('kaze ga tsuyoku fuiteiru',       'kaze ga tsuyoku fuiteiru',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False