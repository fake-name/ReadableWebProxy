def extractHuakuryiWordpressCom(item):
	'''
	Parser for 'huakuryi.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
	if 'Manga' in item['tags']:
		return None
	if 'Lyrics' in item['tags']:
		return None

	tagmap = [
		('Saikyou no Kishidan',                             'Saikyou no Kishidan',                                            'translated'),
		('Isekai ni Tobasareta Ossan wa Doko e Iku?',       'Isekai ni Tobasareta Ossan wa Doko e Iku?',                      'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False