def extractMehtranslationsCom(item):
	'''
	Parser for 'mehtranslations.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('paw in paw',                                         'Paw in Paw, Let’s Satisfy Our Desire for Dogs',                                        'translated'),
		('the favoured genius',                                'Space and Rebirth: The Favoured Genius Doctor and Businesswoman',                      'translated'),
		('the favoured genius doctor and businesswoman',       'Space and Rebirth: The Favoured Genius Doctor and Businesswoman',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False