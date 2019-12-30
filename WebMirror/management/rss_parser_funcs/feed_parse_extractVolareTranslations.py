def extractVolareTranslations(item):
	"""
	'Volare Translations'
	also
	'Volare Novels'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	
	if 'Rotten Recommendations' in item['tags']:
		return None
	if 'volare Creative' in item['tags']:
		return None


	tagmap = [
		("Age of Lazurite",                                             "Age of Lazurite, Tower of Glass",                                                     'translated'),
		("Return of the Swallow",                                       "Return of the Swallow",                                                               'translated'),
		("God of Illusions",                                            "God of Illusions",                                                                    'translated'),
		("Apartment from Hell",                                         "Apartment from Hell",                                                                 'translated'),
		("Divine Throne of Primordial Blood",                           "Divine Throne of Primordial Blood",                                                   'translated'),
		("Blood Hourglass",                                             "Blood Hourglass",                                                                     'translated'),
		("Celestial Employee",                                          "Celestial Employee",                                                                  'translated'),
		("Cultivation Chat Group",                                      "Cultivation Chat Group",                                                              'translated'),
		("Demon Wang's Favorite Fei",                                   "Demon Wang's Golden Favorite Fei",                                                    'translated'),
		("Evil Emperor's Wild Consort",                                 "Evil Emperor's Wild Consort",                                                         'translated'),
		("Falling Dreams of Fang Hua",                                  "Falling Dreams of Fang Hua",                                                          'translated'),
		("Fleeting Midsummer",                                          "Fleeting Midsummer",                                                                  'translated'),
		("Gourmet Food Supplier",                                       "Gourmet Food Supplier",                                                               'translated'),
		("Great Demon King",                                            "Great Demon King",                                                                    'translated'),
		("Hidden Marriage",                                             "Hidden Marriage",                                                                     'translated'),
		("History's Strongest Senior Brother",                          "History's Strongest Senior Brother",                                                  'translated'),
		("I'm Hui Tai Lang",                                            "I'm Hui Tai Lang",                                                                    'translated'),
		("King of Hell",                                                "King of Hell",                                                                        'translated'),
		("My Wife is a Beautiful CEO",                                  "My Wife is a Beautiful CEO",                                                          'translated'),
		("Paradise of the Demons and Gods",                             "Paradise of the Demons and Gods",                                                     'translated'),
		("Pivot of the Sky",                                            "Pivot of the Sky",                                                                    'translated'),
		("Poison Genius Consort",                                       "Poison Genius Consort",                                                               'translated'),
		("Poisoning the World",                                         "Poisoning the World: The Secret Service Mysterious Doctor is a Young Beastly Wife",   'translated'),
		("Prodigal Alliance Head",                                      "Prodigal Alliance Head",                                                              'translated'),
		("Reign of the Hunters",                                        "Reign of the Hunters",                                                                'translated'),
		("Release that Witch",                                          "Release that Witch",                                                                  'translated'),
		("Sovereign of the Three Realms",                               "Sovereign of the Three Realms",                                                       'translated'),
		("Special Forces Spirit",                                       "Special Forces Spirit",                                                               'translated'),
		("Star Rank Hunter",                                            "Star Rank Hunter",                                                                    'translated'),
		("Sword Spirit",                                                "Sword Spirit",                                                                        'translated'),
		("The Nine Cauldrons",                                          "The Nine Cauldrons",                                                                  'translated'),
		("Red Packet Server",                                           "Red Packet Server",                                                                   'translated'),
		("True Cultivators",                                            "The Strong, The Few, True Cultivators on Campus",                                     'translated'),
		("Doomed to be Cannon Fodder",                                  "Doomed to be Cannon Fodder",                                                          'translated'),
		("Adorable Creature Attack",                                    "Adorable Creature Attacks! The Beauty Surrenders!",                                   'translated'),
		("Paradise of Demonic Gods",                                    "Paradise of Demonic Gods",                                                            'translated'),
		("Destroyer of Ice and Fire",                                   "Destroyer of Ice and Fire",                                                           'translated'),
		("Still Wait For Me",                                           "Still, Wait For Me",                                                                  'translated'),
		("Supernatural Girlfriend",                                     "Supernatural Girlfriend",                                                             'translated'),
		("Bone Painting Coroner",                                       "Bone Painting Coroner",                                                               'translated'),
		("This MC Is Kickass",                                          "This MC Is Kickass",                                                                  'translated'),
		("Unruly Phoenix Xiaoyao",                                      "Unruly Phoenix Xiaoyao",                                                              'translated'),
		("Transmigrator Meets Reincarnator",                            "Transmigrator Meets Reincarnator",                                                    'translated'),
		("The Sketch Artist",                                           "The Sketch Artist",                                                                   'translated'),
		("Split Zone 13",                                               "Split Zone No.13",                                                                    'translated'),
		("Phoenix Ascending",                                           "Phoenix Ascending",                                                                   'translated'),
		("Sundering Nature",                                            "Sundering Nature",                                                                    'translated'),
		("Transmigration: Of Mysteries and Songs",                      "Transmigration: Of Mysteries and Songs",                                              'translated'),
		("Killer Nights",                                               "Killer Nights",                                                                       'translated'),
		("The Sword and The Shadow",                                    "The Sword and The Shadow",                                                            'translated'),
		("show me the money",                                           "Show Me the Money",                                                                   'translated'),
		("Lost Treasure",                                               "Lost Treasure",                                                                       'translated'),
		("Rebirth of a Star",                                           "Rebirth of a Star: Another Day, Another Drama",                                       'translated'),
		("Defiant Martial God",                                         "Defiant Martial God",                                                                 'translated'),
		("Rebirth of a Star: Another Day, Another Drama",               "Rebirth of a Star: Another Day, Another Drama",                                       'translated'),
		("Still, Wait For Me",                                          "Still, Wait For Me",                                                                  'translated'),
		("Rebirth of a Fashionista: This Life Is Soo Last Season",      "Rebirth of a Fashionista: This Life Is Soo Last Season",                              'translated'),
		("Fields of Gold",                                              "Fields of Gold",                                                                      'translated'),
		("Consort of a Thousand Faces",                                 "Consort of a Thousand Faces",                                                         'translated'),
		("Song of Exile",                                               "Song of Exile",                                                                       'translated'),
		("The Godking's Legacy",                                        "The Godking's Legacy",                                                                'translated'),
		("Adorable Creature Attacks",                                   "Adorable Creature Attacks! The Beauty Surrenders!",                                   'translated'),
		("the godking’s legacy",                                        "The Godking\'s Legacy",                                                               'oel'),
		("The Dao of Magic",                                            "The Dao of Magic",                                                                    'oel'),
		("Grace Time",                                                  "Grace Time",                                                                          'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	titlemap = [
		('CCG Chapter',                             'Cultivation Chat Group',                                                            'translated'),
		('HTL Chapter',                             'I’m Hui Tai Lang',                                                                  'translated'),
		('YH Chapter',                              'Your Highness',                                                                     'translated'),
		('PTW: SSMD',                               'Poisoning the World: The Secret Service Mysterious Doctor is a Young Beastly Wife', 'translated'),
		('PTW : SSMD',                              'Poisoning the World: The Secret Service Mysterious Doctor is a Young Beastly Wife', 'translated'),
		('ROTH Chapter',                            'Reign of the Hunters',                                                              'translated'),
		('FM Chapter',                              'Fleeting Midsummer Chapter',                                                        'translated'),
		('FM Chapter',                              'Fleeting Midsummer',                                                                'translated'),
		('Hidden Marriage Chapter',                 'Full Marks Hidden Marriage: Pick Up a Son, Get a Free Husband',                     'translated'),
		('DWGMSFF Chapter',                         'Demon Wangs Favorite Fei',                                                          'translated'),
		('The Nine Cauldrons Chapter',              "The Nine Cauldrons",                                                                'translated'),
		('Paradise of the Demons and Gods Chapter', "Paradise of the Demons and Gods",                                                   'translated'),
		('DTPB Chapter',                            "Divine Throne of Primordial Blood",                                                 'translated'),
		('Red Packet Server Chapter',               "Red Packet Server",                                                                 'translated'),
		('Reign of the Hunters Chapter',            "Reign of the Hunters",                                                              'translated'),
		('PGC Chapter',                             "Poison Genius Consort",                                                             'translated'),
		('Fleeting Midsummer Chapter',              "Fleeting Midsummer",                                                                'translated'),
		('Killer Nights Chapter',                   "Killer Nights",                                                                     'translated'),
		
		# Sigh
		('DPTB Chapter',                            "Divine Throne of Primordial Blood",                                                 'translated'),
		('DTPB Chapter',                            "Divine Throne of Primordial Blood",                                                 'translated'),
		('EEWC Chapter',                            "Evil Emperor's Wild Consort",                                                       'translated'),
		('SS Chapter',                              "Sword Spirit",                                                                      'translated'),
		('DIF Chapter',                             "Destroyer of Ice and Fire",                                                         'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if item['title'].startswith(titlecomponent):
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



	return False