def extractNovelsChill(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	# Dunno what 'FiLI' and 'TSM' are, but they seem to have been removed.
	if 'FiLI' in item['tags']:
		return None
	if 'TSM' in item['tags']:
		return None
		

	tagmap = [
		('Abandoned Empress',                                             'Phoenix Overlooking the World – Who Dares to Touch My Abandoned Empress',  "translated"),
		('DHM',                                                           'Dungeon+Harem+Master',                                              "translated"),
		('SULB',                                                          'Skill Up with Login Bonus',                                         "translated"),
		('Aoa',                                                           'Ace of Ace',                                                        "translated"),
		('Aoa',                                                           'Ace of Ace',                                                        "translated"),
		('EER',                                                           'Everyone Else is a Returnee',                                       "translated"),
		('Common Sense of a Duke’s Daughter',                             'Common Sense of a Duke’s Daughter',                                 "translated"),
		('Nozomanu Fushi No Boukensha',                                   'Nozomanu Fushi no Boukensha',                                       "translated"),
		('Everyone Else is a Returnee',                                   'Everyone Else is a Returnee',                                       "translated"),
		('TMoS',                                                          'The Master of Strength',                                            "translated"),
		('EoSP',                                                          'Emperor of Solo Play',                                              "translated"),
		('EIF',                                                           'Everlasting Immortal Firmament',                                    "translated"),
		('Atelier Tanaka',                                                'Atelier Tanaka',                                                    "translated"),
		('Emperor of Solo Play',                                          'Emperor of Solo Play',                                              "translated"),
		('ILBP',                                                          'I Leveled up from Being a Parasite, But I May Have Grown Too Much', "translated"),
		('I Leveled From Being a Parasite',                               'I Leveled up from Being a Parasite, But I May Have Grown Too Much', "translated"),
		('R8CM',                                                          'Revolution of the 8th Class Mage',                                  "translated"),
		('Revolution of the 8th Class Mage',                              'Revolution of the 8th Class Mage',                                  "translated"),
		('TWoA',                                                          'The Wizard of Arecenia',                                            "translated"),
		('The Mightiest Manager',                                         'The Mightiest Manager',                                             "translated"),
		('TMM',                                                           'The Mightiest Manager',                                             "translated"),
		('TTM',                                                           'The Mightiest Manager',                                             "translated"),
		('Have A Meal Before You Go',                                     'Have A Meal Before You Go',                                         "translated"),
		('SkuWLB',                                                        'Skill Up with Login Bonus',                                         "translated"),
		('Skill Up with Login Bonus',                                     'Skill Up with Login Bonus',                                         "translated"),
		('Ace of Ace',                                                    'Ace of Ace',                                                        "translated"),
		('Hello Heir',                                                    'Hello, Heir',                                                       "translated"),
		('Eat Then Leave',                                                'Eat Then Leave',                                                    "translated"),
		('The Reckless Trap Magician',                                    'The Reckless Trap Magician',                                        "translated"),
		('Beast Piercing The Heavens',                                    'Beast Piercing The Heavens',                                        "translated"),
		('Half-Tried Deity',                                              'Half-Tried Deity',                                                  "translated"),
		('Beloved Empress',                                               'Beloved Empress',                                                   "translated"),
		('Xian Wang Dotes On Wife',                                       'Xian Wang Dotes On Wife',                                           "translated"),
		('Portal of Wonderland',                                          'Portal of Wonderland',                                              "translated"),
		('Zombie Evolution',                                              'Zombie Evolution',                                                  "translated"),
		('Seirei Gensouki ~Konna Sekai de Deaeta Kimi ni~',               'Seirei Gensouki ~Konna Sekai de Deaeta Kimi ni~',                   "translated"),
		('The Favored Intelligent Concubine',                             'The Favored Intelligent Concubine',                                 "translated"),
		('Ore no Isekai Shimai ga Jichou Shinai!',                        'Ore no Isekai Shimai ga Jichou Shinai!',                            "translated"),
		('The Spear User that Couldn’t Become the Hero 《Protagonist》',  'The Spear User that Couldn’t Become the Hero 《Protagonist》',      "translated"),
		('Death is The Beginning',                                        'Death is The Beginning',                                            "translated"),
		('Refusing To Serve Me? Then Off With Your Head!',                'Refusing To Serve Me? Then Off With Your Head!',                    "translated"),
		('Your Majesty Please Calm Down',                                 'Your Majesty Please Calm Down',                                     "translated"),
		('The Homebody\'s Lover',                                         'The Homebody\'s Lover',                                             "translated"),
		('Fantasial Apocalypse',                                          'Fantasial Apocalypse',                                              "oel"),
		('Chaotic Emperor',                                               'Chaotic Emperor',                                                   "oel"),
		('CE',                                                            'Chaotic Emperor',                                                   "oel"),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	titlemap = [
		('Emperor of Solo Play Chapter ', 'Emperor of Solo Play',            'translated'),
		('EIF',                           'Everlasting Immortal Firmament',  'translated'),
		('TSM',                           'The Skill Maker',                 'translated'),
		('NFB',                           'Nozomanu Fushi No Boukensha',     'translated'),
		
		('Taming of Yandere',             'The Taming of the Yandere',       'translated'),
		('Taming of the Yandere',         'The Taming of the Yandere',       'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if 'Yandere' in item['title'] and 'Yandere' in titlecomponent:
			print(titlecomponent.lower(), item['title'].lower(), titlecomponent.lower() in item['title'].lower())
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


		
	return False