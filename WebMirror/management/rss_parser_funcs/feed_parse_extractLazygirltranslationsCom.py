def extractLazygirltranslationsCom(item):
	'''
	Parser for 'lazygirltranslations.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
		
	tagmap = [
		('The End Of The World’s Poisonous Mom And Monster Baby',       'The End Of The World’s Poisonous Mom And Monster Baby',                      'translated'),
		('Father, Mother Escaped Again',                                'Father, Mother Escaped Again',                                               'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		

	chp_prefixes = [
			('PMMB Chapter ',  'The End Of The World’s Poisonous Mom And Monster Baby',               'translated'),
		]

	for prefix, series, tl_type in chp_prefixes:
		if item['title'].lower().startswith(prefix.lower()):
			return buildReleaseMessageWithType(item, series, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False