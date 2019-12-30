def extractLainconnueEbisutranslationsCom(item):
	'''
	Parser for 'lainconnue.ebisutranslations.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Unlimited Anime Works',        'Unlimited Anime Works',                       'translated'),
		('Holistic Fantasy',             'Holistic Fantasy',                            'translated'),
		('Shoujo Grand Summoning',       'Shoujo Grand Summoning',                      'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False