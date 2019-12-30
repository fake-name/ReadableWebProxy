def extractCardboardtranslationsCom(item):
	'''
	Parser for 'cardboardtranslations.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	chp_prefixes = [
			('JM ',          'A Demon Lord\'s Tale: Dungeons, Monster Girls, and Heartwarming Bliss',      'translated'),
			('TSKD ',        'Tensei Shitara Ken Deshita',                                                 'translated'),
		]

	for prefix, series, tl_type in chp_prefixes:
		if item['title'].lower().startswith(prefix.lower()):
			return buildReleaseMessageWithType(item, series, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



	return False