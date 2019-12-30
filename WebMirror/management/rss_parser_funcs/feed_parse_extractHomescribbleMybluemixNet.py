def extractHomescribbleMybluemixNet(item):
	'''
	Parser for 'homescribble.mybluemix.net'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Great Tang Idyll Translations',       'Great Tang Idyll',                      'translated'),
		('Great Tang Idyll Chapters',           'Great Tang Idyll',                      'translated'),
		('GTI',                                 'Great Tang Idyll',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False