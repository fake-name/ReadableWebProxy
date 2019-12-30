def extractKobatoChanDaiSukiScan(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Lookism' in item['tags']:
		return None
	if  'webtoon' in item['tags']:
		return None
	if '*Announcements*' in item['tags']:
		return None
	if '*STAFF ONLY*' in item['tags']:
		return None
		
	tagmap = [
		("Can't Stop Craving Potions Again and Again",     "Can't Stop Craving Potions Again and Again",                        'translated'),
		("Can't Stop Craving Potions",                     "Can't Stop Craving Potions",                                        'translated'),
		("Royal Roader on My Own",                         "Royal Roader on My Own",                                            'translated'),
		('A Bird That Drinks Tears',                       'A Bird That Drinks Tears',                                          'translated'),
		('All Things Wrong',                               'Doing All Things Wrong And Somehow Becoming The Best In The Game',  'translated'),
		('Cheat Skill: Sleep Learning',                    'Cheat Skill: Sleep Learning',                                       'translated'),
		('Coder Lee YongHo',                               'Coder Lee YongHo',                                                  'translated'),
		('FFF-Class Trashero',                             'FFF-Class Trashero',                                                'translated'),
		('Dragon Poor',                                    'Dragon Poor',                                                       'translated'),
		('Everyone Else is a Returnee',                    'Everyone Else is a Returnee',                                       'translated'),
		('God of Cooking',                                 'God of Cooking',                                                    'translated'),
		('God of Crime',                                   'God of Crime',                                                      'translated'),
		('God of Music',                                   'God of Music',                                                      'translated'),
		('God of Thunder',                                 'God of Thunder',                                                    'translated'),
		('God-level Bodyguard in the City',                'God-level Bodyguard in the City',                                   'translated'),
		('Green Skin',                                     'Green Skin',                                                        'translated'),
		('I am the monarch',                               'I am the Monarch',                                                  'translated'),
		('Kenkyo kenjitsu o motto ni ikite orimasu!',      'Kenkyo, Kenjitsu o Motto ni Ikite Orimasu!',                        'translated'),
		('Life of the Damned',                             'Life of the Damned',                                                'translated'),
		('Forest of Funerals',                             'Forest of Funerals',                                                'translated'),
		('Link the Orc',                                   'Link the Orc',                                                      'translated'),
		('maou no hajimekata',                             'Maou no Hajimekata',                                                'translated'),
		('Miracle Drawing!',                               'Miracle Drawing!',                                                  'translated'),
		('Omni Genius',                                    'Omni Genius',                                                       'translated'),
		('Omocha no Kyousou-sama',                         'Omocha no Kyousou-sama',                                            'translated'),
		('One Man Army',                                   'One Man Army',                                                      'translated'),
		('Reincarnator',                                   'Reincarnator',                                                      'translated'),
		('Rise Strongest Warrior',                         'Rise Strongest Warrior',                                            'translated'),
		('Solo Clear',                                     'Solo Clear',                                                        'translated'),
		('Survival World RPG',                             'Survival World RPG',                                                'translated'),
		('Ten Thousand Heaven Controlling Sword',          'Ten Thousand Heaven Controlling Sword',                             'translated'),
		('The Bird That Drinks Tears',                     'The Bird That Drinks Tears',                                        'translated'),
		('The Sorcerer Laughs in the Mirror',              'The Sorcerer Laughs in the Mirror',                                 'translated'),
		('The Stone of Days',                              'The Stone of Days',                                                 'translated'),
		('The Strongest System',                           'The Strongest System',                                              'translated'),
		('Wagahai no Kare wa Baka de aru',                 'Wagahai no Kare wa Baka de aru',                                    'translated'),
		('When The Star Flutters',                         'When The Star Flutters',                                            'translated'),
		('Magician of Insa-Dong',                          'Magician of Insa-Dong',                                             'translated'),
		
		("Hero",                                           "Hero",                                                              'oel'),
		("Immortal Ascension Tower",                       "Immortal Ascension Tower",                                          'oel'),
		("The Overlord's Elite is now a Human?!",          "The Overlord's Elite is now a Human?!",                             'oel'),
		("Titan's Throne",                                 "Titan's Throne",                                                    'oel'),
		('Conquest',                                       'Conquest',                                                          'oel'),
		('The Empyrean Nethervoid',                        'The Empyrean Nethervoid',                                           'oel'),
	]

	for tag, sname, tl_type in tagmap:
		if tag in item['tags']:
			return buildReleaseMessageWithType(item, sname, vol, chp, frag=frag, tl_type=tl_type)


	titlemap = [
		('fujimaru wrote a new post, FFF-Class Trashero - Chapter',                  'FFF-Class Trashero',                                                  'translated'),
		('kobatochandaisuki wrote a new post, I Am the Monarch - Chapter',           'I Am the Monarch',                                                    'translated'),
		('Engebu wrote a new post, I Am the Monarch - Chapter',                      'I Am the Monarch',                                                    'translated'),
		('Calvis wrote a new post, Dragon Poor - Chapter',                           'Dragon Poor',                                                         'translated'),
		('Calvis wrote a new post, Green Skin - Chapter',                            'Green Skin',                                                          'translated'),
		('Calvis wrote a new post, Rise, Strongest Warrior - Chapter',               'Rise, Strongest Warrior',                                             'translated'),
		('Calvis wrote a new post, The Stone of Days - ',                            'The Stone of Days',                                                   'translated'),
		('Calvis wrote a new post, The Stone of Days - Chapter',                     'The Stone of Days',                                                   'translated'),
		('csvtranslator wrote a new post, I Am the Monarch - Chapter',               'I Am the Monarch',                                                    'translated'),
		('Koukouseidesu wrote a new post, Everyone Else is a Returnee - Chapter',    'Everyone Else is a Returnee',                                         'translated'),
		('kuhaku wrote a new post, Solo Clear - Chapter ',                           'Solo Clear',                                                          'translated'),
		('miraclerifle wrote a new post, God of Cooking - Chapter',                  'God of Cooking',                                                      'translated'),
		('miraclerifle wrote a new post, Royal Roader on My Own - Chapter',          'Royal Roader on My Own',                                              'translated'),
		('pyrenose wrote a new post, Rise, Strongest Warrior - Chapter',             'Rise, Strongest Warrior',                                             'translated'),
		('Saquacon wrote a new post, All Things Wrong - Chapter',                    'Doing All Things Wrong And Somehow Becoming The Best In The Game',    'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



		
	return False