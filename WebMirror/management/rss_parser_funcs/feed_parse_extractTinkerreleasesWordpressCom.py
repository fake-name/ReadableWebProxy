def extractTinkerreleasesWordpressCom(item):
	'''
	Parser for 'tinkerreleases.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('wce',       'Wife Can’t Escape',                                                 'translated'),
		('DEM',       'The Downfall of the Eldest Miss',                                   'translated'),
		('pmcp',      'Pampering My Cute Pet',                                             'translated'),
		('ismf',      'I am not fit to be the Stubborn Male Lead’s First Love',            'translated'),
		('mdm',       'Married to a Disabled Man in the 70s',                              'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False