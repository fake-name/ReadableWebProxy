def extractSugarbabiesscansWordpressCom(item):
	'''
	Parser for 'sugarbabiesscans.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('evelyn, the red moon',                        'evelyn, the red moon',                                       'translated'),
		('baby hostage\'s so cute',                     'baby hostage\'s so cute',                                    'translated'),
		('surviving as an illegitimate princess',       'surviving as an illegitimate princess',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False