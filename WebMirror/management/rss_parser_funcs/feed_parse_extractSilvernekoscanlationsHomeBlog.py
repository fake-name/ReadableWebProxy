def extractSilvernekoscanlationsHomeBlog(item):
	'''
	Parser for 'silvernekoscanlations.home.blog'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	chp_prefixes = [
			('Who Dares Slander My Senior Brother Chapter ',  'Who Dares Slander My Senior Brother',               'translated'),
			('SCSG Chapter ',                                 'Strategy to Capture that Scum Gong',                'translated'),
			('ASV Chapter ',                                  'A Smile From The Villain',                          'translated'),
		]

	for prefix, series, tl_type in chp_prefixes:
		if item['title'].lower().startswith(prefix.lower()):
			return buildReleaseMessageWithType(item, series, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



	return False