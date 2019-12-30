def extractRei435984511WordpressCom(item):
	'''
	Parser for 'rei435984511.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None


	if item['tags'] != ['Tak Berkategori']:
		return False


	chp_prefixes = [
			('The villager Who Grew Up Drinking Elixir Fountain ',  'The villager Who Grew Up Drinking Elixir Fountain',               'translated'),
			('Another World Transfer in Game Character Episode ',   'Another World Transfer in Game Character',                        'translated'),
			('Manowa',  'Manowa Mamono Taosu Nouryoku Ubau Watashi Tsuyokunaru',               'translated'),
			('Cat ',    'Me and My Beloved Cat (Girlfriend)',                                  'translated'),
		]

	for prefix, series, tl_type in chp_prefixes:
		if item['title'].lower().startswith(prefix.lower()):
			return buildReleaseMessageWithType(item, series, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



	return False