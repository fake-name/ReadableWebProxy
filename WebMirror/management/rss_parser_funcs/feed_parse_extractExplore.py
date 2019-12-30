def extractExplore(item):
	"""
	Explore
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
		
	chp_prefixes = [
			('geww ',                                                                'Ghost Emperor Wild Wife: Dandy Eldest Miss',                                         'translated'),
			('VGAFH',                                                                'Village girl as head of the family: picked up a general for farming',                'translated'),
			('The Rebirth of Deceased Consort that Astounded the World chapter ',    'The Rebirth of Deceased Consort that Astounded the World',                           'translated'),
			('Man Man Qing Luo chapter ',                                            'Man Man Qing Luo',                                                                   'translated'),
			('Hilarious Pampered Consort ',                                          'Hilarious Pampered Consort',                                                         'translated'),
		]

	for prefix, series, tl_type in chp_prefixes:
		if item['title'].lower().startswith(prefix.lower()):
			return buildReleaseMessageWithType(item, series, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


		
	if item['title'].lower().startswith('geww '):
		return buildReleaseMessageWithType(item, 'Ghost Emperor Wild Wife: Dandy Eldest Miss', vol, chp, frag=frag, postfix=postfix)
	return False