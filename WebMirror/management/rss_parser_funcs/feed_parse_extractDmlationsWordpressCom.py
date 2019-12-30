def extractDmlationsWordpressCom(item):
	'''
	Parser for 'dmlations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('The Promise Sealed with our Lips',       'The Promise Sealed with our Lips',                      'translated'),
		('RSCB',                                   'Rebirth of the Supreme Celestial Being',                'translated'),
		('Seizing Dreams',                         'Seizing Dreams',                                        'translated'),
		('sd',                                     'Seizing Dreams',                                        'translated'),
		('NENH',                                   'New Era, New Hell',                                     'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False