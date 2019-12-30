def extractBeammeupscottysstuffWordpressCom(item):
	'''
	Parser for 'beammeupscottysstuff.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('A Change of Pace',       'A Change of Pace',                      'oel'),
		('Two Worlds',             'Two Worlds',                            'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False