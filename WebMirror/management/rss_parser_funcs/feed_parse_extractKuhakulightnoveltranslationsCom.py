def extractKuhakulightnoveltranslationsCom(item):
	'''
	Parser for 'kuhakulightnoveltranslations.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	if item['tags'] != ['Uncategorized']:
		return False
		
	chp_prefixes = [
			('This Time, I Became The Fiance Of A Duke’s Daughter. But She Is Rumored To Have Bad Personality And Ten Years Older ',  'This Time, I Became The Fiance Of A Duke’s Daughter. But She Is Rumored To Have Bad Personality And Ten Years Older',               'translated'),
			
		]

	for prefix, series, tl_type in chp_prefixes:
		if item['title'].lower().startswith(prefix.lower()):
			return buildReleaseMessageWithType(item, series, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


		


	return False