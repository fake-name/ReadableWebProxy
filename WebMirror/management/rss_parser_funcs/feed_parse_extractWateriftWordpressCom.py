def extractWateriftWordpressCom(item):
	'''
	Parser for 'waterift.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Noire de Plaisir',                                 'Noire de Plaisir ~ Pleasure Training of the Fallen Vampire Princess~',                      'translated'),
		('I Have The Only Ero Knowledge In The World',       'I Have The Only Ero Knowledge In The World, So I Decided To Cum Inside Pretty Girls',       'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False