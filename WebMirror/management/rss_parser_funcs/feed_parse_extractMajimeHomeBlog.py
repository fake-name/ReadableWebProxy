def extractMajimeHomeBlog(item):
	'''
	Parser for 'majime.home.blog'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	if item['tags'] == ['Uncategorized']:
		chp_prefixes = [
				('Chapter ',  'Strange Grief Wants to Retire ~The Weakest Hunter’s Hero Dream~',               'translated'),
				('Manowa',  'Manowa Mamono Taosu Nouryoku Ubau Watashi Tsuyokunaru',               'translated'),
				('Cat ',    'Me and My Beloved Cat (Girlfriend)',                                  'translated'),
			]
	
		for prefix, series, tl_type in chp_prefixes:
			if item['title'].lower().startswith(prefix.lower()):
				return buildReleaseMessageWithType(item, series, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



	return False