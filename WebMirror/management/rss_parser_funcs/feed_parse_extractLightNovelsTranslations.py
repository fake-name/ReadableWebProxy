def extractLightNovelsTranslations(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
		
		
		
	tagmap = [
		('I Just About Became a Living Cheat when Raising My Level in the Real Life',  'I Just About Became a Living Cheat when Raising My Level in the Real World',               'translated'),
		('I Became a Living Cheat',                                                    'I Just About Became a Living Cheat when Raising My Level in the Real World',               'translated'),
		('HimeKishi Ga Classmate!',                                                    'Himekishi ga Classmate! ~ Isekai Cheat de Dorei ka Harem~',                                'translated'),
		('Re:Master Magic',                                                            'The Mage Will Master Magic Efficiently In His Second Life',                                'translated'),
		('The Man Who Would Be King',                                                  'The Man Who Would Be King',                                                                'translated'),
		('Man Eating Dungeon',                                                         'Hitokui Dungeon e Youkoso',                                                                'translated'),
		('maou no hajimekata',                                                         'Maou no Hajimekata',                                                                       'translated'),
		('Pure Love x Insult Complex',                                                 'Pure Love x Insult Complex',                                                               'translated'),
		('Charging Magic with a Smile',                                                'Charging Magic with a Smile',                                                              'translated'),
		('Yuusha ni Horobosareru',                                                     'Yusha ni Horobosareru Dake no Kantan na Oshigoto Desu',                                    'translated'),
		('The 5000 Year Old Herbivorous Dragon',                                       'The 5000 Year Old Herbivorous Dragon',                                                     'translated'),
		('My Sister the Heroine, and I the Villainess',                                'My Sister the Heroine, and I the Villainess',                                              'translated'),
		('Different World Gender Change',                                              'It Seems That I\'ve Slipped Into a Different World. Also, My Gender Has Changed.',         'translated'),
		('The Sweets Prince\'s Search',                                                'The Sweets Prince\'s Search',                                                              'translated'),
		('I Got a Cheat, So I Want to Live as I Like',                                 'I Got a Cheat, So I Want to Live as I Like',                                               'translated'),
		('The Summoner is Going',                                                      'The Summoner is Going',                                                                    'translated'),
		('Dragon-san Wants a Friend',                                                  'Dragon-san Wants a Friend',                                                                'translated'),
		('over the infinite',                                                          'over the infinite',                                                                        'translated'),
		('Fiancée of the Wizard',                                                      'Fiancée of the Wizard',                                                                    'translated'),
		('galactic navy officer',                                                      'Kochugunshikan Boukensha ni Naru',                                                         'translated'),
		('Fairy Tale Chronicles',                                                      'Fairy Tale Chronicles',                                                                    'translated'),
		('space mercenary',                                                            'I Woke Up Piloting the Strongest Starship, so I Became a Space Mercenary',                 'translated'),
		('goodbye dragon life, hello human life',                                      'goodbye dragon life, hello human life',                                                    'translated'),
		('Heavenly Castle',                                                            'Heavenly Castle',                                                                          'translated'),
		('Shiinamachi-senpai\'s Safe Day',                                             'Shiinamachi-senpai\'s Safe Day',                                                           'translated'),
		('Nidome no Yuusha',                                                           'Nidome no Yuusha',                                                                         'translated'),
		('Elf Tensei',                                                                 'From Elf Reincarnation to Cheat Kingdom Founding Chronicle',                               'translated'),
		('The Strongest Wizard',                                                       'The Strongest Wizard Becomes a Countryside Guardsman After Taking an Arrow to the Knee',   'translated'),
		('Tsunpri: Aishite Ohimesama',                                                 'Tsunpri: Aishite Ohimesama',                                                               'translated'),
		('inyouchuu',                                                                  'Inyouchuu ~Exorcisms of the Lewd School~',                                                 'translated'),
		('rule breaker',                                                               'The Undetectable Strongest Job: Rule Breaker',                                             'translated'),
		('100 things about my senpai',                                                 '100 Things I Don\'t Know About My Senior',                                                 'translated'),
		('the dropout swordsman',                                                      'I Realised that I Became The Strongest After Spamming the 100 Million Years Button – The Dropout Swordsman that Became Unparalleled',           'translated'),
		('shangrila frontier',                                                         'ShangriLa Frontier ~ Shitty Games Hunter Challenges Godly Game ~',                         'translated'),
		('slave harem in fantasy world',                                               'slave harem in fantasy world',                                                             'translated'),
		('Road to Kingdom',                                                            'Road to Kingdom',                                                                          'translated'),
		('Different World Reincarnation as a Sage',                                    'Different World Reincarnation as a Sage',                                                  'translated'),
		('The Hidden Dungeon Only I can Enter',                                        'The Hidden Dungeon Only I can Enter',                                                      'translated'),
		('House Magic',                                                                'My House is a Magic Power Spot~ Just by Living there I Become the Strongest in the World', 'translated'),
		('Dragon Knight to Carrier',                                                   'From The Strongest Job of Dragon Knight, To The Beginner Job Carrier, Somehow, The Heroes are Depending on Me', 'translated'),
		('apostle of the gods',                                                        'Apostle of the Gods',                                                                      'oel'),
		('Ruler',                                                                      'Ruler',                                                                                    'oel'),
		('the advent of death’s daughter',                                             'The Advent of Death’s Daughter',                                                           'oel'),
		('the demon lord’s redemption',                                                'The Demon Lord’s Redemption',                                                              'oel'),
		('emotional defect',                                                           'Emotional Defect',                                                                         'oel'),
		('The Pagemasters',                                                            'The Pagemasters',                                                                          'oel'),
		('return of the fallen',                                                       'Return of the Fallen',                                                                     'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)
		
	return False