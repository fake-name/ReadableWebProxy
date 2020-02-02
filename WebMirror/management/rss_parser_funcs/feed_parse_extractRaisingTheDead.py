def extractRaisingTheDead(item):
	"""
	# extractRaisingTheDead

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
		
	if 'The RTD Story' in item['tags']:
		return None	
	if 'RTD Story' in item['tags']:
		return None		
	if 'origins' in item['tags']:
		return None	
	if 'recruitment' in item['tags']:
		return None
	if 'What Side Didn\'t Know' in item['tags']:
		return None
		
	if 'KmF?!' in item['tags']:
		matches = re.search('When I returned home, what I found was fantasy!\\? (\\d+)\\-(\\d+)', item['title'], flags=re.IGNORECASE)
		if matches:
			vol = float(matches.group(1))
			chp = float(matches.group(2))
			return buildReleaseMessageWithType(item, 'Kaettekite mo Fantasy!?', vol, chp, frag=frag, postfix=postfix)
	if 'Takami no Kago' in item['title']:
		return buildReleaseMessageWithType(item, 'Takami No Kago', vol, chp, frag=frag)
	if item['title'].startswith('slave harem'):
		return buildReleaseMessageWithType(item, 'Isekai Meikyuu De Dorei Harem wo', vol, chp, frag=frag)
	if 'Shinka' in item['title']:
		return buildReleaseMessageWithType(item, 'Shinka no Mi', vol, chp, frag=frag)
	if 'Smartphone Chapter' in item['title']:
		return buildReleaseMessageWithType(item, 'Isekai wa Smartphone to Tomoni', vol, chp, frag=frag)
	if 'Tran Sexual Online' in item['title']:
		return buildReleaseMessageWithType(item, 'Tran Sexual Online', vol, chp, frag=frag)
	if 'Trans Sexual Online' in item['title']:
		return buildReleaseMessageWithType(item, 'Tran Sexual Online', vol, chp, frag=frag)
	if 'Master Of Monsters' in item['title']:
		return buildReleaseMessageWithType(item, 'Master Of Monsters', vol, chp, frag=frag)
	if item['title'].startswith('(R18) Frequenting Brothels'):
		return buildReleaseMessageWithType(item, 'Game nai ni haitte Dragon o Hanto Shinagara Shokan ni Kayoi Tsumeru Hanashi.', vol, chp, frag=frag)


	tagmap = [

		('OreMegane',                                               'Ore no Megane wa tabun Sekai Seifuku Dekiru to Omou',                                      'translated'),
		('Alice Tales',                                             'Alice Tale in Phantasmagoria',                                                             'translated'),
		('Average Abilities',                                       'I Said Make My Abilities Average!',                                                        'translated'),
		('wakamo',                                                  'Wakamo',                                                                                   'translated'),
		('Slave Harem',                                             'Slave Harem',                                                                              'translated'),
		('Din No Monshou',                                          'Din No Monshou',                                                                           'translated'),
		('E? Heibon Desu Yo??',                                     'E? Heibon Desu Yo??',                                                                      'translated'),
		('Eh? Heibon desu yo??',                                    'E? Heibon Desu Yo??',                                                                      'translated'),
		('Elf Tensei',                                              'Elf Tensei Kara no Cheat Kenkoku-ki',                                                      'translated'),
		('Game nai ni haitte Doragon o hanto',                      'Game nai ni haitte Dragon o Hanto Shinagara Shokan ni Kayoi Tsumeru Hanashi.',             'translated'),
		('Hachinan tte Sore wa nai Deshou!',                        'Hachinan tte Sore wa nai Deshou!',                                                         'translated'),
		('I Said Make My Abilities Average!',                       'I Said Make My Abilities Average!',                                                        'translated'),
		('Iisekai no mahou gengo ga doumitemo nihongo dattaken',    'No matter how you look at it, this world\'s magic language is Japanese.',                  'translated'),
		('Invincible Magician',                                     'Invincible Magician ~ Akashic Record Overwrite~',                                          'translated'),
		('RW(I)FP',                                                 'Reincarnated With (In)Finite Power',                                                       'oel'),
		('My Bodyguard Can\'t Fight Girls',                         'My Bodyguard Can\'t Fight Girls',                                                          'oel'),
		('A Tails Misfortune',                                      'A Tail\'s Misfortune',                                                                     'oel'),
		('A Tail\'s Misfortune',                                    'A Tail\'s Misfortune',                                                                     'oel'),
		('The Search for Knowledge',                                'The Search for Knowledge',                                                                 'oel'),
		('attack 0 crit all',                                       'My attack stat is negligible, so I can’t help but rely on critical attacks to succeed',    'oel'),
		('ascension',                                               'Ascension',                                                                                'oel'),
		('Talentless Beast Knight',                                 'Talentless Beast Knight',                                                                  'oel'),
		('The Search for Knowledge',                                'The Search for Knowledge',                                                                 'oel'),
		('Sword Detective Hayate',                                  'Sword Detective Hayate',                                                                   'oel'),
		('Is Heaven Supposed To Be Like This?!',                    'Is Heaven Supposed to Be Like This?!',                                                     'oel'),
		('Isekai meikyuu de dorei harem wo',                        'Isekai Meikyuu De Dorei Harem wo',                                                         'translated'),
		('Katte Kita Motoyuusha',                                   'Katte Kita Motoyuusha',                                                                    'translated'),
		('Kumo desu ga',                                            'Kumo Desu Ga, Nani Ka?',                                                                   'translated'),
		('Master of Monster',                                       'Master Of Monsters',                                                                       'translated'),
		('Master of Monsters',                                      'Master Of Monsters',                                                                       'translated'),
		('Right Grasper',                                           'Right Grasper ~Stealing Skills in the Other World~',                                       'translated'),
		('Riot Grasper',                                            'Riot Grasper',                                                                             'translated'),
		('Science shall Prevail over Magic - Overture',             'Science shall Prevail over Magic - Overture',                                              'translated'),
		('Science Shall Prevail over Magic',                        'Science shall Prevail over Magic',                                                         'translated'),
		('Shinka no Mi',                                            'Shinka no Mi',                                                                             'translated'),
		('Skill Taker',                                             'Skill Taker',                                                                              'translated'),
		('Slave harem in the labyrinth of the other world',         'Isekai Meikyuu De Dorei Harem wo',                                                         'translated'),
		('Smartphone',                                              'Isekai wa Smartphone to Tomoni',                                                           'translated'),
		('I have Unlimited Wives Slots',                            'I have Unlimited Wives Slots',                                                             'translated'),
		('Kaette Kita no Motoyuusha',                               'Kaette Kita no Motoyuusha',                                                                'translated'),
		('Takami no Kago',                                          'Takami No Kago',                                                                           'translated'),
		('Tran Sexual Online',                                      'Tran Sexual Online',                                                                       'translated'),
		('Undergroud Doctor',                                       'Underground Doctor',                                                                       'translated'),
		('Underground Doctor',                                      'Underground Doctor',                                                                       'translated'),
		('Yuusha Ga Onna Da to Dame Desu Ka?',                      'Yuusha Ga Onna Da to Dame Desu Ka?',                                                       'translated'),
		('OP Waifu',                                                'Being Able to Edit Skills in Another World, I Gained OP Waifus',                           'translated'),
		('owmb',                                                    'Isekai Monster Breeder',                                                                   'translated'),
		('Motoyuusha',                                              'Return of Former Hero',                                                                    'translated'),


		('I, with house work and cooking, takes away the backbone of the Demon lord! The peerless house-husband starts from kidnapping!',   
			'I, with house work and cooking, takes away the backbone of the Demon lord! The peerless house-husband starts from kidnapping!', 'translated'),
		("Demon Lord's Pet",                                                                                                                
			'I, with house work and cooking, takes away the backbone of the Demon lord! The peerless house-husband starts from kidnapping!', 'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False