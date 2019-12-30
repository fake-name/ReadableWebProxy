def extractLanguidtranslationsBlogspotCom(item):
	'''
	Parser for 'languidtranslations.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	if item['tags'] != []:
		return False
		
	chp_prefixes = [
			('Unrepentant ',  'Unrepentant',               'translated'),
			('Deposed Empress General ',  'Deposed Empress General',               'translated'),
		]

	for prefix, series, tl_type in chp_prefixes:
		if item['title'].lower().startswith(prefix.lower()):
			return buildReleaseMessageWithType(item, series, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



	return False