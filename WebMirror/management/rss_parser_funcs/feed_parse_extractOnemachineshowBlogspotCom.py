def extractOnemachineshowBlogspotCom(item):
	'''
	Parser for 'onemachineshow.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('amdtvba',       'After My Death, The Villain Blackened Again',                      'translated'),
		('ebed',          'Quick Transmigration: Ex-Girlfriend Blackens Every Day',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False