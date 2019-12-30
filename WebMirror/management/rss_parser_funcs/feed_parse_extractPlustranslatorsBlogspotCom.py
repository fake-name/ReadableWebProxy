def extractPlustranslatorsBlogspotCom(item):
	'''
	Parser for 'plustranslators.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	chp_prefixes = [
			('Artifact Planting Space Chapter',  'Artifact Planting Space',               'translated'),
			('Manowa',  'Manowa Mamono Taosu Nouryoku Ubau Watashi Tsuyokunaru',               'translated'),
			('Cat ',    'Me and My Beloved Cat (Girlfriend)',                                  'translated'),
		]

	for prefix, series, tl_type in chp_prefixes:
		if item['title'].lower().startswith(prefix.lower()):
			return buildReleaseMessageWithType(item, series, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



	tagmap = [
		('Artifact planting space',       'Artifact planting space',                      'translated'),
		('Overgod Ascension',             'Overgod Ascension',                            'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False