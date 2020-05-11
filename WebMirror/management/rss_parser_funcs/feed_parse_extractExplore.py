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
			('BTTS ',                                                                'Back to the Sixties: Farm, Get Wealthy & Raise the Cubs',                            'translated'),
			('Campus Rebirth: The Strongest Female Agent',                           'Campus Rebirth: The Strongest Female Agent',                                         'translated'),
			('ESWHYMY ',                                                             'Eldest Sister, Why Haven\'t You Married Yet',                                        'translated'),
			('TVHISLAA ',                                                            'Today Villain Husband Is Still Lying About Amnesia (Novel Transmigration)',          'translated'),
			('Transmigrated into the Cannon Fodder\'s Daughter ',                    'Transmigrated into the Cannon Fodder\'s Daughter',                                   'translated'),
		]

	for prefix, series, tl_type in chp_prefixes:
		if item['title'].lower().startswith(prefix.lower()):
			return buildReleaseMessageWithType(item, series, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


		
	if item['title'].lower().startswith('geww '):
		return buildReleaseMessageWithType(item, 'Ghost Emperor Wild Wife: Dandy Eldest Miss', vol, chp, frag=frag, postfix=postfix)
	return False