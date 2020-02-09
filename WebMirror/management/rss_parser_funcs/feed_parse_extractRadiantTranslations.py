def extractRadiantTranslations(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Announcements' in item['tags'] or 'schedule' in item['tags']:
		return None
		

	tagmap = [
		('Truly Precious Shared Universe',               'Truly Precious Shared Universe',                         'translated'),
		('Great Demon King',                             'Great Demon King',                                       'translated'),
		('Xyrin Empire',                                 'Xyrin Empire',                                           'translated'),
		('Amnesiac Queen',                               'Amnesiac Queen',                                         'translated'),
		('Beautiful Girl Poison Doctor Third Miss',      'Beautiful Girl Poison Doctor Third Miss',                'translated'),
		('Death Sutra',                                  'Death Sutra',                                            'translated'),
		('My World Falls into the River of Love',        'My World Falls into the River of Love',                  'translated'),
		('Ghost Emperor Wild Wife',                      'Ghost Emperor Wild Wife',                                'translated'),
		('Heavenly Calamity',                            'Heavenly Calamity',                                      'translated'),
		('Unrepentant',                                  'Unrepentant',                                            'translated'),
		('Pivot of the Sky',                             'Pivot of the Sky',                                       'translated'),
		('Lord Xue Ying',                                'Lord Xue Ying',                                          'translated'),
		('Dragon Emperor Martial God',                   'Dragon Emperor Martial God',                             'translated'),
		('Battle Frenzy',                                'Battle Frenzy',                                          'translated'),
		('Ostentatious Zhao Yao',                        'Ostentatious Zhao Yao',                                  'translated'),
		('The Whirlwind Girl 1: The Beginning of Light', 'The Whirlwind Girl 1: The Beginning of Light',           'translated'),
		('Magic Chef of Ice and Fire',                   'Magic Chef of Ice and Fire',                             'translated'),
		('The Legend of the Dragon King',                'The Legend of the Dragon King',                          'translated'),
		('Zither Emperor',                               'Zither Emperor',                                         'translated'),
		('Evil Dragon Against the Heaven',               'Evil Dragon Against the Heaven',                         'translated'),
		('Radiant Era',                                  'Radiant Era',                                            'translated'),
		('Miracle Throne',                               'Miracle Throne',                                         'translated'),
		('The Alchemist God',                            'The Alchemist God',                                      'translated'),
		('Village Girl as Family Head',                  'Village Girl as Family Head',                            'translated'),
		('Lord Xue Ying',                                'Xue Ying Ling Zhu',                                      'translated'),
		('Child of Light',                               'Guang Zhi Zi',                                           'translated'),
		('Celestial Emperor Han',                        'Celestial Emperor Han',                                  'translated'),
		('Guang Zhi Zi',                                 'Guang Zhi Zi',                                           'translated'),
		('Bing Huo Mo Chu',                              'Bing Huo Mo Chu',                                        'translated'),
		('Magic Chef of Ice and Fire',                   'Bing Huo Mo Chu',                                        'translated'),
		('The Legend of the Dragon King',                'Xue Ying Ling Zhu',                                      'translated'),
		('Beautiful Girl: Poison Doctor Third Miss',     'Beautiful Girl: Poison Doctor Third Miss',               'translated'),
		('Tempest of the Stellar War',                   'Tempest of the Stellar War',                             'translated'),
		('Dragon Marked War God',                        'Dragon-Marked War God',                                  'translated'),
		('I Seem Unsuited for Dating',                   'I Seem Unsuited for Dating',                             'translated'),
		('Sweet Heart in Honeyed Desire',                'Sweet Heart in Honeyed Desire',                          'translated'),
		('Enchantress Among Alchemists',                 'Enchantress Amongst Alchemists: Ghost King’s Concubine', 'translated'),
		('The Whirlwind Girl',                           'The Whirlwind Girl 1: The Beginning of Light',           'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	if 'dragon marked war god' in item['title'].lower().replace('-', ' '):
		return buildReleaseMessageWithType(item, 'Dragon-Marked War God', vol, chp, frag=frag, postfix=postfix)
		
	titlemap = [
		('dmwg',                                                          'Dragon-Marked War God',                                  'translated'),
		('beseech the devil',                                             'Beseech the Devil',                                      'translated'),
		('enchantress amongst alchemist: ghost king’s concubine chapter', 'Enchantress Amongst Alchemists: Ghost King’s Concubine', 'translated'),
		('Enchantress Amongst Alchemists: Ghost King’s Wife Chapter',     'Enchantress Amongst Alchemists: Ghost King’s Concubine', 'translated'),
		('enchantress amongst alchemists: ghost king’s concubine',        'Enchantress Amongst Alchemists: Ghost King’s Concubine', 'translated'),
		('Evil Dragon Against the Heaven Chapter',                        'Evil Dragon Against the Heaven',                         'translated'),
		('Evil Dragon Against the Heavens Chapter',                       'Evil Dragon Against the Heaven',                         'translated'),
		('Miracle Throne Chapter',                                        'Miracle Throne',                                         'translated'),
		('Death Sutra – Chapter',                                         'Death Sutra',                                            'translated'),
		('Battle Frenzy – Chapter',                                       'Battle Frenzy',                                            'translated'),
		('Zither Emperor –',                                              'Zither Emperor',                                            'translated'),
		
		('Lord Xue Ying',                              'Xue Ying Ling Zhu',                                                                     'translated'),
		('GEWW',                                       'Ghost Emperor Wild Wife: Dandy Eldest Miss',                                            'translated'),
		('VGAFH',                                      'Village Girl as the Head of the Family: Picked Up a General for Farming',               'translated'),
		('Radiant Era',                                'Radiant Era',                                                                           'translated'),
		('Magic Chef of Ice and Fire',                 'Magic Chef of Ice and Fire',                                                            'translated'),
		('The Legend of the Dragon King',              'The Legend of the Dragon King',                                                         'translated'),
		('Tempest of the Stellar War',                 'Tempest of the Stellar War',                                                            'translated'),

	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)





	return False