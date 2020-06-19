def extractOrientalrabbitWordpressCom(item):
	'''
	Parser for 'orientalrabbit.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('tmrw',       'How Many Tomorrows There Are',                      'translated'),
		('scgl',       'Side Character Survival Guidelines',                'translated'),
		('wlwm',       'A White Lotus Host Who Does Not Want To Be a White Moonlight Is Not a Good Host',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False