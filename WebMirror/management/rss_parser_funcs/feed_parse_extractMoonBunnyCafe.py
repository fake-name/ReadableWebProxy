def extractMoonBunnyCafe(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	bad_titles = [
			'Nekomata ', 
			'Nigemichi wa Kochira - ', 
			'Curse Note - ', 
			'Hi Ni Iru - ', 
			'Kaidan Tochuu no Big Noise', 
			'preview'
		]

	if any([bad_title in item['title'] for bad_title in bad_titles]):
		return None
		
	if 'announcements' in item['tags']:
		return None
	if 'Manhwa' in item['tags']:
		return None


	tlut = {
		
		"dragon's bloodline"                                                             : "Dragon's Bloodline",
		"shura's wrath"                                                                  : "Shura's Wrath",
		"the guild's cheat receptionist"                                                 : "The Guild's Cheat Receptionist",
		"what's your gender, princess?"                                                  : "What's Your Gender, Princess?",
		'a lonesome fragrance waiting to be appreciated'                                 : 'A Lonesome Fragrance Waiting to be Appreciated',
		'accompanying the phoenix'                                                       : 'Accompanying the Phoenix',
		'against the gods'                                                               : 'Against The Gods',
		'and so the girl obtained a wicked girl’s body'                                  : "And so the Girl Obtained a Wicked Girl's Body",
		'apartments for rent'                                                            : 'Apartments for Rent',
		'b group no shounen'                                                             : 'B Group no Shounen',
		'because i’m a weapon shop uncle'                                                : "Because I'm a Weapon Shop Uncle",
		'bewitching prince spoils his wife: genius doctor unscrupulous consort'          : 'Bewitching Prince Spoils His Wife: Genius Doctor Unscrupulous Consort',
		'bewitching prince spoils his wife: genius doctor unscrupulous consort'          : 'Bewitching Prince Spoils His Wife: Genius Doctor Unscrupulous Consort',
		'black bellied prince’s stunning abandoned consort'                              : 'Black Bellied Prince’s Stunning Abandoned Consort',
		'Boku wa Isekai de Fuyo Mahou to Shoukan Mahou wo Tenbin ni Kakeru'              : "Boku wa Isekai de Fuyo Mahou to Shoukan Mahou wo Tenbin ni Kakeru",
		'botsuraku youtei nanode, kajishokunin wo mezasu'                                : 'Botsuraku Youtei Nanode, Kajishokunin wo Mezasu',
		'boundary labyrinth and the foreign magician'                                    : 'Boundary Labyrinth and the Foreign Magician',
		'bringing a farm to mess around in another world'                                : 'Bringing A Farm To Mess Around In Another World',
		'bringing a farm'                                                                : 'Bringing A Farm To Mess Around In Another World',
		'cat k'                                                                          : 'Cat K',
		'cultivating to become a great celestial'                                        : 'Cultivating to Become a Great Celestial',
		'doctor of the demon world'                                                      : 'Doctor of the Demon World',
		'dragon\'s bloodline'                                                            : 'Dragon\'s Bloodline',
		'dual sword liberator'                                                           : 'Dual Sword Liberator',
		'e mei (beauty)'                                                                 : 'E Mei (Beauty)',
		'empress running away with the ball!'                                            : 'Empress Running Away with the Ball!',
		'five way heaven'                                                                : 'Five Way Heaven',
		'five way heaven'                                                                : 'Five Way Heaven',
		'genius doctor : black belly miss'                                               : 'Genius Doctor: Black Belly Miss',
		'Ghostly Masked Prince Xiao: Pampering and Spoiling the Little Adorable Consort' : 'Ghostly Masked Prince Xiao: Pampering and Spoiling the Little Adorable Consort',
		'god of thunder'                                                                 : 'God of Thunder',
		'godly hunter'                                                                   : 'Godly Hunter',
		'heavenly star'                                                                  : 'Heavenly Star',
		'i became an in-game npc'                                                        : 'I Became an In-game NPC',
		'i decided to not compete and quietly create dolls instead'                      : 'I Decided to Not Compete and Quietly Create Dolls Instead',
		'i reincarnated as a noble girl villainess, but why did it turn out this way'    : 'I Reincarnated as a Noble Girl Villainess, but why did it turn out this way',
		'i reincarnated as a noble girl villainess, but why did it turn out this way?'   : 'I Reincarnated as a Noble Girl Villainess, but why did it turn out this way',
		'i, am playing the role of the older brother in hearthrob love revolution'       : 'I, am Playing the Role of the Older Brother in Heart-throb Love Revolution.',
		'insanely pampered wife: divine doctor fifth young miss'                         : 'Insanely Pampered Wife: Divine Doctor Fifth Young Miss',
		'inside the cave of obscenity'                                                   : 'Inside the Cave of Obscenity',
		'invincible saint ~salaryman, the path i walk to survive in this other world~'   : 'Invincible Saint ~Salaryman, the path I walk to survive in this other world~',
		'isekai maou to shoukan shoujo dorei majutsu'                                    : 'Isekai Maou to Shoukan Shoujo no Dorei Majutsu',
		'island: end of nightmare'                                                       : 'Island: End of Nightmare',
		'it seems like i got reincarnated into the world of a yandere otome game.'       : 'It seems like I got reincarnated into the world of a Yandere Otome game.',
		'it seems like i got reincarnated into the world of a yandere otome game.'       : 'It seems like I got reincarnated into the world of a Yandere Otome game.',
		'i’ll live my second life!'                                                      : 'I’ll Live My Second Life!',
		'i’m a neet but when i went to hello work i got taken to another world'          : 'I’m a NEET but when I went to Hello Work I got taken to another world',
		'i’m a neet but when i went to hello work i got taken to another world'          : 'NEET dakedo Hello Work ni Ittara Isekai ni Tsuretekareta',
		'kamigoroshi no eiyuu to nanatsu no seiyaku'                                     : 'Kamigoroshi no Eiyuu to Nanatsu no Seiyaku',
		'kumo desu ga, nani ka?'                                                         : 'Kumo Desu ga, Nani ka?',
		'kuro no maou'                                                                   : 'Kuro no Maou',
		'lazy dungeon master'                                                            : 'Lazy Dungeon Master',
		'lazy dungeon master'                                                            : 'Lazy Dungeon Master',
		'legend'                                                                         : 'Legend',
		'm e m o r i z e'                                                                : 'M E M O R I Z E',
		'magic mechanics shuraba'                                                        : 'Magic Mechanics Shuraba',
		'magic robot aluminare'                                                          : 'Magic Robot Aluminare',
		'maken no daydreamer'                                                            : 'Maken no Daydreamer',
		'monogatari no naka no hito'                                                     : 'Monogatari no Naka no Hito',
		'muimui-tan'                                                                     : 'Muimui-Tan',
		'muimui-tan'                                                                     : 'Muimui-Tan',
		'my disciple died yet again'                                                     : 'My Disciple Died Yet Again',
		'my favorable rating does not rise'                                              : 'My Favorable Rating Does Not Rise',
		'no fatigue'                                                                     : 'No Fatigue',
		'omni-magician'                                                                  : 'Omni-Magician',
		'otherworld nation founding'                                                     : 'Otherworld Nation Founding Chronicles',
		'parallel world pharmacy'                                                        : 'Parallel World Pharmacy',
		'Poison the World'                                                               : 'Poisoning the World: The Secret Service Mysterious Doctor is a Young Beastly Wife',
		'purple river'                                                                   : 'Purple River',
		'rebirth of the thief who roamed the world'                                      : 'Rebirth of the Thief Who Roamed the World',
		'running away from the hero!'                                                    : 'Running Away From The Hero!',
		'sendai yuusha wa inkyou shitai'                                                 : 'Sendai Yuusha wa Inkyou Shitai',
		'shen mu'                                                                        : 'Shen Mu',
		'single player only'                                                             : 'single player only',
		'slave career planner'                                                           : 'Slave Career Planner', 
		'story of a careless demon'                                                      : 'Story of a Careless Demon',
		'tensei shitara slime datta ken'                                                 : 'Tensei Shitara Slime Datta Ken',
		'the bears bear a bare kuma'                                                     : 'The Bears Bear a Bare Kuma',
		'the cry of the phoenix which reached the ninth heaven'                          : 'The Cry of the Phoenix Which Reached the Ninth Heaven',
		'the demonic king chases his wife: the rebellious good-for-nothing miss'         : 'The Demonic King Chases His Wife: The Rebellious Good-for-nothing Miss', 
		'the saint’s recovery magic is a degraded version of mine'                       : 'The Saint’s Recovery Magic is a Degraded Version of Mine',
		'the simple life of killing demons'                                              : 'The Simple Life of Killing Demons',
		'Evil Emperor\'s Poisonous Consort: Divine Doctor Young Miss'                    : 'Evil Emperor\'s Poisonous Consort: Divine Doctor Young Miss',
		'Transmigrated into Another World with an Unparalleled System'                   : 'Transmigrated into Another World with an Unparalleled System',
		'Heaven\'s Will Balancing System'                                                : 'Heaven\'s Will Balancing System',
		'time'                                                                           : 'Time',
		'Unprecedented Pill Refiner: Entitled Ninth Young Lady'                          : 'Unprecedented Pill Refiner: Entitled Ninth Young Lady',
		'wife is outrageous: his evil highness comes knocking'                           : 'Wife is Outrageous: His Evil Highness Comes Knocking',
		'xiao qi, wait'                                                                  : 'Xiao Qi, Wait',
		'GOD LEVEL DEMON'                                                                : 'God Level Demon',
	}



	etlut = {
		'Overseer' : 'Overseer'

	}
	
	
	ltags = [tmp.lower() for tmp in item['tags']]

	if 'manhwa' in ltags or 'manhua' in ltags or 'manga' in ltags:
		return None
	
	
	# Patch lower case names so I don't have to bother lower-casing
	# them manually
	for key, value in list(tlut.items()):
		tlut[key.lower()] = value

			
	for key, value in etlut.items():
		if key in ltags:
			return buildReleaseMessageWithType(item, value, vol, chp, frag=frag, postfix=postfix, tl_type='oel')

	for key, value in tlut.items():
		if key in ltags:
			return buildReleaseMessageWithType(item, value, vol, chp, frag=frag, postfix=postfix)
			
			
			
			

	cleaned_title = item['title'].lower().replace('’', '').replace("'", '') 
			
	if cleaned_title.startswith("enl "):
		return buildReleaseMessageWithType(item, 'Unprecedented Pill Refiner: Entitled Ninth Young Lady', vol, chp, frag=frag, postfix=postfix)
	if cleaned_title.startswith("legend "):
		return buildReleaseMessageWithType(item, 'Legend', vol, chp, frag=frag, postfix=postfix)
	if cleaned_title.startswith("overseer "):
		return buildReleaseMessageWithType(item, 'Overseer', vol, chp, frag=frag, postfix=postfix, tl_type='oel')

	if 'accompanying the phoenix' in cleaned_title and 'chapter' in cleaned_title:
		return buildReleaseMessageWithType(item, 'Accompanying the Phoenix', vol, chp, frag=frag, postfix=postfix)

	titlemap = [
		('because im a weapon shop uncle',                                            "Because I'm a Weapon Shop Uncle",                                                    'translated'),
		('because im a weapons shop uncle',                                           "Because I'm a Weapon Shop Uncle",                                                    'translated'),
		('dkc chapter',                                                               'The Demonic King Chases His Wife: The Rebellious Good-for-nothing Miss',             'translated'),
		('boku wa isekai de fuyo mahou to shoukan mahou wo tenbin ni kakeru chapter', 'Boku wa Isekai de Fuyo Mahou to Shoukan Mahou wo Tenbin ni Kakeru',                  'translated'),
		('slave career planner volume',                                               'Slave Career Planner',                                                               'translated'),
		('parallel world pharmacy',                                                   'Parallel World Pharmacy',                                                            'translated'),
		('world record',                                                              'World Record',                                                                       'translated'),
		('empress running away with the ball',                                        'Empress Running Away with the Ball',                                                 'translated'),
		('the guilds cheat receptionist',                                             "The Guild's Cheat Receptionist",                                                     'translated'),
		('gdbbm',                                                                     "Genius Doctor : Black Belly Miss",                                                   'translated'),
		('bewitching prince spoils his wife',                                         'Bewitching Prince Spoils His Wife',                                                  'translated'),
		('xqw',                                                                       'Xiao Qi, Wait',                                                                      'translated'),
		('cbgc',                                                                      'Cultivating to Become a Great Celestial',                                            'translated'), 
		('careless demon',                                                            'Demon Noble Girl ~Story of a Careless Demon~',                                       'translated'),
		('memorize',                                                                  'M E M O R I Z E',                                                                    'translated'),
		('godly hunter',                                                              'Godly Hunter',                                                                       'translated'),
		('accompanying the phoenix',                                                  'Accompanying The Phoenix',                                                           'translated'),
		('weapon shop uncle',                                                         'Because I\'m a Weapon Shop Uncle',                                                   'translated'),
		('invincible saint ',                                                         'Invincible Saint ~Salaryman, the path I walk to survive in this other world~',       'translated'),
		('bbps consort',                                                              'Black Bellied Prince’s Stunning Abandoned Consort',                                  'translated'),
		('wife is outrageous',                                                        'Wife is Outrageous: His Evil Highness Comes Knocking',                               'translated'),
		('muimui-tan',                                                                'Muimui-tan',                                                                         'translated'), 
		('got ',                                                                      'God of Thunder',                                                                     'translated'),
		('she was both called god',                                                   'She was both called God, as well as Satan',                                          'translated'),
		('common sense of a dukes daughter ',                                         'Common Sense of a Duke\'s Daughter',                                                 'translated'),
		('poisoning the world',                                                       'Poisoning the World: The Secret Service Mysterious Doctor is a Young Beastly Wife',  'translated'),
		('bewitching prince chapter',                                                 'Bewitching Prince Spoils His Wife: Genius Doctor Unscrupulous Consort',              'translated'),
		('ddfym – ',                                                                  'Insanely Pampered Wife: Divine Doctor Fifth Young Miss',                             'translated'),
		('cry of phoenix',                                                            'The Cry of the Phoenix Which Reached the Ninth Heaven',                              'translated'),
		('island vol',                                                                'Island: End of Nightmare',                                                           'translated'),
		('evil emperors poisonous consort: divine doctor young miss chapter',         'Evil Emperor’s Poisonous Consort: Divine Doctor Young Miss',                         'translated'),
		('single player only chapter',                                                'Single Player Only',                                                                 'translated'),
		('kuzu inou chapter ',                                                        'Kuzu Inou【Ondo wo Kaeru Mono】 no Ore ga Musou suru made',                          'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent in cleaned_title:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

			
			
	return False