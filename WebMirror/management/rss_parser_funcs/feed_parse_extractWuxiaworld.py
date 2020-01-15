def extractWuxiaworld(item):
	"""
	# Wuxiaworld

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		print("No Chap/Vol?")
		return None

	if 'Announcements' in item['tags']:
		return None
	if 'Translator Thoughts' in item['tags']:
		return None
	
	if 'Dragon King with Seven Stars' in item['title']:
		return buildReleaseMessageWithType(item, 'Dragon King with Seven Stars', vol, chp, frag=frag)
	if 'BTTH Chapter' in item['title']:
		return buildReleaseMessageWithType(item, 'Battle Through the Heavens', vol, chp, frag=frag)
	if item['title'].startswith('☀COL '):
		return buildReleaseMessageWithType(item, 'Child of Light', vol, chp, frag=frag)
	if item['title'].startswith('♟ WMW Chapter'):
		return buildReleaseMessageWithType(item, 'Warlock of the Magus World', vol, chp, frag=frag)
	if item['title'].startswith('🗡RT Chapter'):
		return buildReleaseMessageWithType(item, 'Rebirth of the Thief', vol, chp, frag=frag)

	if item['tags'] == ['Uncategorized']:
		print("No Tags?")
		return None

	tagmap = [
		("DD2: Unrivaled Tang Sect",                        'Douluo Dalu 2 - The Unrivaled Tang-Clan',           'translated'),
		("Emperor's Domination",                            "Emperor's Domination",                              'translated'),
		('A Record of a Mortal\'s Journey to Immortality',  'A Record of a Mortal\'s Journey to Immortality',    'translated'),
		('Archfiend',                                       'Archfiend',                                         'translated'),
		('A Will Eternal',                                  'A Will Eternal',                                    'translated'),
		('Absolute Choice',                                 'Absolute Choice',                                   'translated'),
		('Acquiring Talent in a Dungeon',                   'Acquiring Talent in a Dungeon',                     'translated'),
		('Against the Gods',                                'Ni Tian Xie Shen',                                  'translated'),
		('Ancient Godly Monarch',                           'Ancient Godly Monarch',                             'translated'),
		('Ancient Strengthening Technique',                 'Ancient Strengthening Technique',                   'translated'),
		('ATG Chapter Release',                             'Ni Tian Xie Shen',                                  'translated'),
		('Battle Through the Heavens',                      'Battle Through the Heavens',                        'translated'),
		('Invincible',                                      'Invincible',                                        'translated'),
		('Breakers',                                        'Breakers',                                          'translated'),
		('BTTH Chapter Release',                            'Battle Through the Heavens',                        'translated'),
		('CD Chapter Release',                              'Coiling Dragon',                                    'translated'),
		('Child of Light',                                  'Child of Light',                                    'translated'),
		('Coiling Dragon',                                  'Coiling Dragon',                                    'translated'),
		('COL Chapter Release',                             'Child of Light',                                    'translated'),
		('DE Chapter Release',                              'Desolate Era',                                      'translated'),
		('Desolate Era',                                    'Desolate Era',                                      'translated'),
		('dragon king with seven stars',                    'Dragon King with Seven Stars',                      'translated'),
		('Dragon Maken War',                                'Dragon Maken War',                                  'translated'),
		('Emperor of Solo Play',                            'Emperor of Solo Play',                              'translated'),
		('Gate of Revelation',                              'The Gate of Revelation',                            'translated'),
		('God of Crime',                                    'God of Crime',                                      'translated'),
		('Infinite Competitive Dungeon Society',            'Infinite Competitive Dungeon Society',              'translated'),
		('Heavenly Jewel Change',                           'Heavenly Jewel Change',                             'translated'),
		('HeavenlyJewelChange',                             'Heavenly Jewel Change',                             'translated'),
		('HJC Chapter Release',                             'Heavenly Jewel Change',                             'translated'),
		('I Really Am A Superstar',                         'I\'m Really a Superstar',                           'translated'),
		('I Shall Seal the Heavens',                        'I Shall Seal the Heavens',                          'translated'),
		('I\'m Really a Superstar',                         'I\'m Really a Superstar',                           'translated'),
		('ISSTH Chapter Release',                           'I Shall Seal the Heavens',                          'translated'),
		('Legend of the Dragon King',                       'Legend of the Dragon King',                         'translated'),
		('Martial God Asura',                               'Martial God Asura',                                 'translated'),
		('Martial World',                                   'Martial World',                                     'translated'),
		('MGA Chapter Release',                             'Martial God Asura',                                 'translated'),
		('Perfect World',                                   'Perfect World',                                     'translated'),
		('Rebirth of the Thief',                            'Rebirth of the Thief',                              'translated'),
		('Renegade Immortal',                               'Renegade Immortal',                                 'translated'),
		('SA Chapter Release',                              'Skyfire Avenue',                                    'translated'),
		('Seoul Station’s Necromancer',                     'Seoul Station\'’s Necromancer',                     'translated'),
		('Skyfire Avenue',                                  'Skyfire Avenue',                                    'translated'),
		('Skyfire Avenue',                                  'Skyfire Avenue',                                    'translated'),
		('SL Chapter Release',                              'Skyfire Avenue',                                    'translated'),
		('Sovereign of the Three Realms',                   'Sovereign of the Three Realms',                     'translated'),
		('Spirit Realm',                                    'Spirit Realm',                                      'translated'),
		('Spirit Vessel',                                   'Spirit Vessel',                                     'translated'),
		('ST Chapter Release',                              'Xingchenbian',                                      'translated'),
		('Imperial God Emperor',                            'Imperial God Emperor',                              'translated'),
		('Stellar Transformations',                         'Stellar Transformations',                           'translated'),
		('Tales of Demons & Gods',                          'Tales of Demons & Gods',                            'translated'),
		('TDG Chapter Release',                             'Tales of Demons & Gods',                            'translated'),
		('Praise the Orc!',                                 'Praise the Orc!',                                   'translated'),
		('Terror Infinity',                                 'Terror Infinity',                                   'translated'),
		('The Book Eating Magician',                        'The Book Eating Magician',                          'translated'),
		('TGR Chapter Release',                             'The Great Ruler',                                   'translated'),
		('The Grandmaster Strategist',                      'The Grandmaster Strategist',                        'translated'),
		('The Great Ruler',                                 'The Great Ruler',                                   'translated'),
		('True Martial World',                              'True Martial World',                                'translated'),
		('Unrivaled Tang Sect',                             'Douluo Dalu 2 - The Unrivaled Tang-Clan',           'translated'),
		('Upgrade Specialist in Another World',             'Upgrade Specialist in Another World',               'translated'),
		('Upgrade Specialist',                              'Upgrade Specialist',                                'translated'),
		('Warlock of the Magus World',                      'Warlock of the Magus World',                        'translated'),
		('The Godsfall Chronicles',                         'The Godsfall Chronicles',                           'translated'),
		('Talisman Emperor',                                'Talisman Emperor',                                  'translated'),
		('Wu Dong Qian Kun',                                'Wu Dong Qian Kun',                                  'translated'),
		('Charm of Soul Pets',                              'The Charm of Soul Pets',                            'translated'),
		('Dragon Talisman',                                 'Dragon Talisman',                                   'translated'),
		('Overgeared',                                      'Overgeared',                                        'translated'),
		('Lord of All Realms',                              'Lord of All Realms',                                'translated'),
		('Monarch of Evernight',                            'Monarch of Evernight',                              'translated'),
		('I Reincarnated for Nothing',                      'I Reincarnated for Nothing',                        'translated'),
		('The Charm of Soul Pets',                          'The Charm of Soul Pets',                            'translated'),
		('Nine Star Hegemon Body Art',                      'Nine Star Hegemon Body Art',                        'translated'),
		('Dragon Prince Yuan',                              'Dragon Prince Yuan',                                'translated'),
		('Demon Hunter',                                    'Demon Hunter',                                      'translated'),
		('Divine Throne of Primordial Blood',               'Divine Throne of Primordial Blood',                 'translated'),
		('City of Sin',                                     'City of Sin',                                       'translated'),
		('Condemning the Heavens',                          'Condemning the Heavens',                            'translated'),
		('Rebirth of the Thief Who Roamed the World',       'Rebirth of the Thief Who Roamed the World',         'translated'),
		('The Novel\'s Extra',                              'The Novel\'s Extra',                                'translated'),
		('Trash of the Count\'s Family',                    'Trash of the Count\'s Family',                      'translated'),
		('Stop, Friendly Fire!',                            'Stop, Friendly Fire!',                              'translated'),
		('the second coming of gluttony',                   'the second coming of gluttony',                     'translated'),
		('Sage Monarch',                                    'Sage Monarch',                                      'translated'),
		('Martial Star Ocean',                              'Martial Star Ocean',                                'translated'),
		('Everlasting',                                     'Everlasting',                                       'translated'),
		('Red Storm',                                       'Red Storm',                                         'translated'),
		('TranXending Vision',                              'TranXending Vision',                                'translated'),
		('Emperor’s Domination',                            'Emperor’s Domination',                              'translated'),
		('I\'m sorry for being born',                       'I\'m Sorry For Being Born In This World!',          'translated'),
		('I’m Sorry For Being Born In This World!',         'I\'m Sorry For Being Born In This World!',          'translated'),
		('heaven\'s devourer',                              'Swallowing the Heavens',                            'translated'),
		('physician’s odyssey',                             'Physician\'s Odyssey',                              'translated'),
		('The Sword and The Shadow',                        'The Sword and The Shadow',                          'translated'),
		('everyone is young except for me',                 'everyone is young except for me',                   'translated'),
		('dungeon predator',                                'dungeon predator',                                  'translated'),
		('almighty sword domain',                           'almighty sword domain',                             'translated'),
		('The Unrivaled Tang Sect',                         'The Unrivaled Tang Sect',                           'translated'),
		('A Record of a Mortal’s Journey to Immortality',   'A Record of a Mortal’s Journey to Immortality',     'translated'),
		
		
		('Overthrowing Fate',                  'Overthrowing Fate',            'oel'),
		('The Divine Elements',                'The Divine Elements',          'oel'),
		('Blue Phoenix',                       'Blue Phoenix',                 'oel'),
		('Legends of Ogre Gate',               'Legends of Ogre Gate',         'oel'),
	
	]
	
	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			if 'nothing' in item['title'].lower():
				print("building release: ", name, vol, chp, frag)
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



		
	return False