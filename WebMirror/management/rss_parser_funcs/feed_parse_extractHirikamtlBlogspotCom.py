def extractHirikamtlBlogspotCom(item):
	'''
	Parser for 'hirikamtl.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('OTOGE',       'I Don’t Want to Die in an Otome Game',                      'translated'),
		('MWP',         'My Wolf Prince',                      'translated'),
		('Kurousa',     'The Black Healing Holy Beast ~Is What It Is Exaggeratedly Called but It Is Just a Black Rabbit~',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False