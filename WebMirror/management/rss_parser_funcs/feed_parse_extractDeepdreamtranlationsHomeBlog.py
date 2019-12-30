def extractDeepdreamtranlationsHomeBlog(item):
	'''
	Parser for 'deepdreamtranlations.home.blog'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('The Scum Shou\'s Survival Guide',                 'The Scum Shou\'s Survival Guide',                      'translated'),
		('TSSSG',                                           'The Scum Shou\'s Survival Guide',                      'translated'),
		('TSWCSS',                                          'The Strategy of Washing Clean a Slag Shou',                      'translated'),
		('The Strategy of Washing Clean a Slag Shou',       'The Strategy of Washing Clean a Slag Shou',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False