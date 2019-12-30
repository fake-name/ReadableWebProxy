def extractWuxiaNation(item):
	"""
	'WuxiaNation'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Announcements' in item['tags']:
		return None
		
	tagmap = [
		('Mysterious Job Called Oda Nobunaga',              'Mysterious Job Called Oda Nobunaga',             'translated'),
		('The Lame Daoist Priest',                          'The Lame Daoist Priest',                         'translated'),
		('I Grow Stronger by Dreaming',                     'I Grow Stronger by Dreaming',                    'translated'),
		('World of Warcraft: Foreign Realm Domination',     'World of Warcraft: Foreign Realm Domination',    'translated'),
		('Storm in the Wilderness',                         'Storm in the Wilderness',                        'translated'),
		('Great Dao Commander',                             'Great Dao Commander',                            'translated'),
		('A Stern Devil',                                   'A Stern Devil',                                  'translated'),
		('Song of Heroes',                                  'Song of Heroes',                                 'translated'),
		('the dark king',                                   'The Dark King',                                  'translated'),
		('age of heroes',                                   'Age of Heroes',                                  'translated'),
		('Conquer God, Asura, and 1000 Beauties',           'Conquer God, Asura, and 1000 Beauties',          'translated'),
		('The Solitary Sword Sovereign',                    'The Solitary Sword Sovereign',                   'translated'),
		('lord shadow',                                     'Lord Shadow',                                    'translated'),
		('In Different World With Naruto System',           'In Different World With Naruto System',          'translated'),
		('Wiro Sableng',                                    'Wiro Sableng',                                   'translated'),
		('7 Kingdoms of Midgard',                           '7 Kingdoms of Midgard',                          'translated'),
		('MOTDN',                                           'Monarch of the Dark Nights',                     'translated'),
		('Hisshou Dungeon Unei Houhou',                     'Hisshou Dungeon Unei Houhou',                    'translated'),
		('nagabumi',                                        'Nagabumi',                                       'translated'),
		('Special Forces King',                             'Special Forces King',                            'translated'),
		('Immortal Ape King',                               'Immortal Ape King',                              'translated'),
		('Law of the Devil',                                'Law of the Devil',                               'translated'),
		('Age of Adventure',                                'Age of Adventure',                               'translated'),
		('Nine Yang Sword Saint',                           'Nine Yang Sword Saint',                          'translated'),
		('warlord',                                         'Warlord',                                        'translated'),
		('MRRG',                                            'My Reality is a Romance Game',                   'translated'),
		('eth2',                                            'Evolution Theory of the Hunter',                 'translated'),
		('eth',                                             'Evolution Theory of the Hunter',                 'translated'),
		('CoR',                                             'Cohen of the Rebellion',                         'translated'),
		('The Assassin\'s Apprentice',                      'The Assassin\'s Apprentice',                     'translated'),
		('Immortal Ascension Tower',                        'Immortal Ascension Tower',                       'oel'),
		('Aurora God',                                      'Aurora God',                                     'oel'),
		('lord shadow',                                     'lord shadow',                                    'oel'),
		('Pathless Origins: Bane of the Gods',              'Pathless Origins: Bane of the Gods',             'oel'),
		('Novus Gaia',                                      'Age of Heroes: Novus Gaia',                      'oel'),
		('House of Omen',                                   'House of Omen',                                  'oel'),
		('Samsara Breaker',                                 'Samsara Breaker',                                'oel'),
		('Venture with Anime system',                       'Venture with Anime system',                      'oel'),
		
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	return False