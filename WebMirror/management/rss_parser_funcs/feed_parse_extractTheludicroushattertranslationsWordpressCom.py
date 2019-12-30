def extractTheludicroushattertranslationsWordpressCom(item):
	'''
	Parser for 'theludicroushattertranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('The Sales Executive\'s New Love Interest',       'The Sales Executive\'s New Love Interest',                      'translated'),
		('Avian Over Gold',                                'Avian Over Gold',                                               'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False