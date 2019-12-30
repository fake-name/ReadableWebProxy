def extractYintranslationsCom(item):
	'''
	Parser for 'yintranslations.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('When I Returned From Another World I Was A Silver Haired Shrine Maiden',       'When I Returned From Another World I Was A Silver Haired Shrine Maiden',                      'translated'),
		('Astarte\'s Knight',                                                            'Astarte\'s Knight',                                                                           'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False