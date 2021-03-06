def extractTakemewithyuuHomeBlog(item):
	'''
	Parser for 'takemewithyuu.home.blog'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('gomene onii-sama',       'Gomen ne, Onii-sama',                      'translated'),
		('ごめんね、お兄様',       'Gomen ne, Onii-sama',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False