def extractIkosyndromeTumblrCom(item):
	'''
	Parser for 'ikosyndrome.tumblr.com'
	'''


	badwords = [
			'Vocaloid',
			'vocaloid song',
			'kpop translation',
			'korean song translation',
			'badword',
		]
	if any([bad in item['tags'] for bad in badwords]):
		return None



	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('fairytale for wizards',        'A Fairytale for Wizards',                      'translated'),
		('a fairytale for wizard',       'A Fairytale for Wizards',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False