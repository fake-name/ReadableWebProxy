def extractShinsori(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	
	if "shinsori.com/glossary/" in item['linkUrl'].lower():
		return None
	
	if 'Patrons' in item['title'] or 'Patreon' in item['title']:
		return None
	if 'Teaser #' in item['title']:
		return None
	if 'Manga' in item['tags']:
		return None

	tag_map = [
		('QA',                                                          'GMs, QA Your Worlds First!',                                                               'oel'),
		('Draconia',                                                    'Draconia',                                                                                 'oel'),
		('Kindred',                                                     'Kindred',                                                                                  'oel'),
		('Charmed?',                                                    'Charmed?',                                                                                 'oel'),
		('Silver Death',                                                'Silver Death',                                                                             'oel'),
		('Silver Death (Re)',                                           'Silver Death (Re)',                                                                        'oel'),
		('Snowborn',                                                    'Snowborn',                                                                                 'oel'),
		
		('Reincarnated Princess',                                       'Reincarnated Princess',                                                                    'translated'),
		('Undead Seeks Warmth',                                         'Undead Seeks Warmth',                                                                      'translated'),
		('Frontiers',                                                   'Frontiers',                                                                                'translated'),
		('Doll Dungeon',                                                'Doll Dungeon',                                                                             'translated'),
		('Boku wa Chiisana Maou-sama',                                  'Boku wa Chiisana Maou-sama',                                                               'translated'),
		('Wagamama Onna ni Tensei Shita yo',                            'Wagamama Onna ni Tensei Shita yo',                                                         'translated'),
		('Race: Various',                                               'Occupation: Adventurer ; Race: Various',                                                   'translated'),
		('100 Cheat Skills',                                            '100 Cheat Skills',                                                                         'translated'),
		('Wagamama Onna',                                               'Wagamama Onna ni Tensei Shita yo',                                                         'translated'),
		('Tensei Reijou',                                               'Tensei Reijou wa Yancha Suru',                                                             'translated'),
		('Yuusha ga Onna',                                              'Yuusha Ga Onna Da to Dame Desu Ka?',                                                       'translated'),
		('Isekai Shoukan ni Makikomareta Obaachan',                     'Isekai Shoukan ni Makikomareta Obaachan',                                                  'translated'),
		('Raising Slaves',                                              'Raising Slaves in Another World While on a Journey',                                       'translated'),
		('Vampire',                                                     'Tensei Shitara Kyuuketsuki-san Datta Ken',                                                 'translated'),
		('Tensei Shitara Kyuuketsuki-san Datta Ken',                    'Tensei Shitara Kyuuketsuki-san Datta Ken',                                                 'translated'),
		('Princess',                                                    'The Great Nation Remodeling of Reincarnated Princess ~Let’s Build an Unrivalled Country~', 'translated'),
		('Isekai Yururi Kikou',                                         'Isekai Yururi Kikou',                                                                      'translated'),
		('Chiisana Maou-sama',                                          'Boku wa Chiisana Maou-sama',                                                               'translated'),
		('Obaachan',                                                    'Isekai Shoukan ni Makikomareta Obaachan',                                                  'translated'),
		('Nigotta Hitomi no Lilianne',                                  'Nigotta Hitomi no Lilianne',                                                               'translated'),
		('Bones',                                                       'Hone no aru Yatsu',                                                                        'translated'),
		('Onsen',                                                       'Isekai Onsen e Youkoso!',                                                                  'translated'),
		('Isekai Tensei',                                               'Isekai Tensei Harem',                                                                      'translated'),
		('Lilianne',                                                    'Nigotta Hitomi no Lilianne',                                                               'translated'),
		('Hone no aru Yatsu',                                           'Hone no aru Yatsu',                                                                        'translated'),
		('Isekai Onsen e Youkoso!',                                     'Isekai Onsen e Youkoso!',                                                                  'translated'),
		('Avoid the Death Route!',                                      'Avoid the Death Route!',                                                                   'translated'),
		('Isekai Tensei Harem',                                         'Isekai Tensei Harem',                                                                      'translated'),
		('The Great Nation Remodeling',                                 'Great Nation Remodeling of a Reincarnated Princess',                                       'translated'),
		('Obaachan (28) is Free',                                       'Obaachan (28) is Free',                                                                    'translated'),
		('the dismissed royal magician is returning home ~the country is a facing crisis, but i don’t care~',                                            'the dismissed royal magician is returning home ~the country is a facing crisis, but i don’t care~',                                                                         'translated'),
		('Isekai Risshiden',                                            'Isekai Risshiden',                                                                         'translated'),
		('Yuusha Ga Onna Da to Dame Desu Ka?',                          'Yuusha Ga Onna Da to Dame Desu Ka?',                                                       'translated'),
		('Tensei Reijou wa Yancha Suru',                                'Tensei Reijou wa Yancha Suru',                                                             'translated'),
		('Raising Slaves in Another World',                             'Raising Slaves on the Other World While on a Journey',                                     'translated'),
		('Swain Hakushaku Reijou',                                      'Swain Hakushaku Reijou no Chiisana Oujisama',                                              'translated'),
		('Mezametara Chikashitsu!?',                                    'Mezametara Chikashitsu!? ~Tensei Shoujo no Yume no Saki~',                                 'translated'),
		('Mezametara Chikashitsu!? ~Tensei Shoujo no Yume no Saki~',    'Mezametara Chikashitsu!? ~Tensei Shoujo no Yume no Saki~',                                 'translated'),
		('Shomin no Aji',                                               'Tensei Reijou wa Shomin no Aji ni Uete Iru',                                               'translated'),
		('tensei reijou ha shomin no aji ni ueteiru',                   'tensei reijou ha shomin no aji ni ueteiru',                                                'translated'),
		('Akuyaku ni Nari Sugita',                                      'Akuyaku ni Nari Sugita',                                                                   'translated'),
		('demon lord wants to laze',                                    'Demon Lord Wants to Laze',                                                                 'translated'),
		('Heroine of the Broken Engagement',                            'Heroine of the Broken Engagement',                                                         'translated'),
		('Child Rearing Hero',                                          'Child Rearing Hero and Children of the Demon King',                                        'translated'),
		('my husband, the commander of imperial guards, wants to divorce me, but i don’t want to part with my angelic stepchild.',        'my husband, the commander of imperial guards, wants to divorce me, but i don’t want to part with my angelic stepchild.',      'translated'),
		('Akuyaku Reijou ni Nanka Narimasen',                                                          'akuyaku reijou ni nanka narimasen. watashi wa『futsuu』no koushaku reijou desu!',                       'translated'),
		('akuyaku reijou ni nanka narimasen. watashi wa『futsuu』no koushaku reijou desu!',            'akuyaku reijou ni nanka narimasen. watashi wa『futsuu』no koushaku reijou desu!',                       'translated'),
		('she retaliated because her entire family was wrongfully executed. and thoroughly at that!',  'she retaliated because her entire family was wrongfully executed. and thoroughly at that!',             'translated'),
	]

	for tag, sname, tl_type in tag_map:
		if tag in item['tags']:
			return buildReleaseMessageWithType(item, sname, vol, chp, frag=frag, tl_type=tl_type)


	title_map = [
		('Kindred',                                            'Kindred',                                                   'oel'),
		('Charmed?',                                           'Charmed?',                                                  'oel'),
		('Silver Death',                                       'Silver Death',                                              'oel'),
		
		('Yuusha ga onna da to dame desu ka?',                 'Yuusha ga onna da to dame desu ka?',                        'translated'),
		('The Bears Bear a Bare Kuma',                         'Kuma Kuma Kuma Bear',                                       'translated'),
		('Kuma Kuma Kuma Bear',                                'Kuma Kuma Kuma Bear',                                       'translated'),
		('Doll Dungeon',                                       'Doll Dungeon',                                              'translated'),
		('Levelmaker –',                                       'Levelmaker -Raising Levels While Living in Another World-', 'translated'),
		('Isekai Tensei Harem',                                'Isekai Tensei Harem',                                       'translated'),
		('Undead Seeks Warmth',                                'Undead Seeks Warmth',                                       'translated'),
		('Raising Slaves in Another World While on a Journey', 'Raising Slaves in Another World While on a Journey',        'translated'),
		('Occupation: Adventurer ; Race: Various',             'Occupation: Adventurer ; Race: Various',                    'translated'),
		('My Engagement was Annulled (lol)',                   'My Engagement was Annulled (lol)',                          'translated'),
		('Akuyaku Reijou ni Nanka Narimasen',                  'Akuyaku Reijou ni Nanka Narimasen. Watashi wa『Futsuu』no Koushaku Reijou desu!',                    'translated'),
	]

	for title_fragment, sname, tl_type in title_map:
		if title_fragment in item['title']:
			return buildReleaseMessageWithType(item, sname, vol, chp, frag=frag, tl_type=tl_type)


	return False