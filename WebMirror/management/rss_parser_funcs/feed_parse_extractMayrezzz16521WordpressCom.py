def extractMayrezzz16521WordpressCom(item):
	'''
	Parser for 'mayrezzz16521.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('the childhood friends that i love secretly for ten years suddenly ask me to come out',       'the childhood friends that i love secretly for ten years suddenly ask me to come out',                      'translated'),
		('when the male supporting actor bend the male lead',                                          'when the male supporting actor bend the male lead',                                                         'translated'),
		('acting school',                                                                              'acting school',                                                                                             'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False