def extractOzfortunaWordpressCom(item):
	'''
	Parser for 'ozfortuna.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('transmigrated canon fodder, please calm down!',       'transmigrated canon fodder, please calm down!',                      'translated'),
		('married to the male lead\'s father',                  'married to the male lead\'s father',                                 'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False