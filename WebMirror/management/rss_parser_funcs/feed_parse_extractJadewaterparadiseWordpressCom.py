def extractJadewaterparadiseWordpressCom(item):
	'''
	Parser for 'jadewaterparadise.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Our Glamorous Time',              'Our Glamorous Time',                             'translated'),
		('Dragon Phoenix and Flower',       'Dragon, Phoenix and Flower',                     'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False