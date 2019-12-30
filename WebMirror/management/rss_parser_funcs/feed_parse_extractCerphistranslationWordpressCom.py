def extractCerphistranslationWordpressCom(item):
	'''
	Parser for 'cerphistranslation.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	chp_prefixes = [
			('BMHS ',  'Beloved Marriage in High Society',               'translated'),
			# ('RJHS ',  'Beloved Marriage in High Society',               'translated'),
			# ('CKDFRA ',  'Beloved Marriage in High Society',               'translated'),
		]

	for prefix, series, tl_type in chp_prefixes:
		if item['title'].lower().startswith(prefix.lower()):
			return buildReleaseMessageWithType(item, series, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False