def extractWwwFuyunekoOrg(item):
	'''
	Parser for 'www.fuyuneko.org'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	chp_prefixes = [
			('ChongFei Manual Ch ',                        'ChongFei Manual',                        'translated'),
			('The Dreamer in the Spring Boudoir - Ch ',    'The Dreamer in the Spring Boudoir',      'translated'),
		]

	for prefix, series, tl_type in chp_prefixes:
		if item['title'].lower().startswith(prefix.lower()):
			return buildReleaseMessageWithType(item, series, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



	return False