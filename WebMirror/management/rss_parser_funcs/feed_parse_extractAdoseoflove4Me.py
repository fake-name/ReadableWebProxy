def extractAdoseoflove4Me(item):
	'''
	Parser for 'adoseoflove4.me'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('The Overbearing Chief Husband\'s Favorite: Baby',                                 'The Overbearing Chief Husband\'s Favorite: Baby',                                                'translated'),
		('Exclusive Property',                                                              'Exclusive Property: Mr. Mu’s Favorite',                                                          'translated'),
		('Exclussive Possession',                                                           'Exclusive Property: Mr. Mu’s Favorite',                                                          'translated'),
		('Long Live the Wild Wife: The Black Bellied Evil King against the Princess',       'Long Live the Wild Wife: The Black Bellied Evil King against the Princess',                      'translated'),
		('LLW',                                                                             'Long Live the Wild Wife: The Black Bellied Evil King against the Princess',                      'translated'),
		('The Overbearing Chief Husband\'s Favorite: Treasure',                             'The Overbearing Chief Husband\'s Favorite: Treasure',                                            'translated'),
		('TOCHB',                                                                           'The Overbearing Chief Husband\'s Favorite: Treasure',                                            'translated'),
		('Exclusive Property: Mr. Mu’s Favorite',                                           'Exclusive Property: Mr. Mu\'s Favorite',                                                         'translated'),
		('ep',                                                                              'Exclusive Property: Mr. Mu\'s Favorite',                                                         'translated'),
		('swdp',                                                                            'The Shadowy Wedding Day with the President',                                                     'translated'),
		('swpf',                                                                            'Uncle’s Super Awesome: Sweet Wife, Pampered Fast',                                               'translated'),
		('mycd',                                                                            'Madam, your vest dropped again',                                                                 'translated'),
		('fymy',                                                                            'Familiarity Breeds Marriage: Mysterious Young Master, Super Cool ',                              'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False