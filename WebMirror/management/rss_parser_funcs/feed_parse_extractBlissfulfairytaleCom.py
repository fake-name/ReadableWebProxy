def extractBlissfulfairytaleCom(item):
	'''
	Parser for 'blissfulfairytale.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('reborn as the villain president\'s lover',       'reborn as the villain president\'s lover',                      'translated'),
		('i raised a sick and weak prince',                'i raised a sick and weak prince',                               'translated'),
		('pretty her [qt]',                                'Pretty Her [QT]',                                               'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False