def extractViolentfluffballWordpressCom(item):
	'''
	Parser for 'violentfluffball.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('The Adonis Next Door: 100 Days of Forced Love',       'The Adonis Next Door: 100 Days of Forced Love',                      'translated'),
		('How To Say I Love You',                               'How To Say I Love You',                                              'translated'),
		('HTSILY',                                              'How To Say I Love You',                                              'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False