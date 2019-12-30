def extractSpicychickentranslationsWordpressCom(item):
	'''
	Parser for 'spicychickentranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Ghosts Know What I Experienced',                             'Ghosts Know What I Experienced',                                            'translated'),
		('The General\'s Manor Young Concubine Survival Report',       'The General\'s Manor Young Concubine Survival Report',                      'translated'),
		('TGMYCSR',                                                    'The General\'s Manor Young Concubine Survival Report',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False