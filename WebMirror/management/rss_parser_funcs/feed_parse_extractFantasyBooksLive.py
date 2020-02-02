def extractFantasyBooksLive(item):
	"""
	fantasy-books.live
	"""
	
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	
	if 'short story' in item['tags']:
		return None
	
	# This series is unparsable, because it has no sane chapter numbering.
	if '69526' in item['tags']:
		return None
	
	

	tagmap = [

		   
		('Champion is Playing',                                                     'Champion is Playing',                                                           'translated'),
		('A Monster Who Levels Up',                                                 'A Monster Who Levels Up',                                                       'translated'),
		('Beloved Empress',                                                         'Beloved Empress',                                                               'translated'),
		('Black Haired King',                                                       'Black Haired King',                                                             'translated'),
		('Castle of Black Iron',                                                    'Castle of Black Iron',                                                          'translated'),
		('Common Sense of a Duke\'s Daughter',                                      'Common Sense of a Duke\'s Daughter',                                            'translated'),
		('Emperor of the North',                                                    'Emperor of the North',                                                          'translated'),
		('Eternal Reverence',                                                       'Eternal Reverence',                                                             'translated'),
		('Girl, I\'ll Teach You Cultivation',                                       'Girl, I\'ll Teach You Cultivation',                                             'translated'),
		('Godfather',                                                               'Godfather',                                                                     'translated'),
		('Godly Student',                                                           'Godly Student',                                                                 'translated'),
		('Grave Robber',                                                            'Grave Robber',                                                                  'translated'),
		('Great Han’s Female General Wei Qiqi',                                     'Great Han\'s Female General Wei Qiqi',                                          'translated'),
		('Hello, Heir!',                                                            'Hello, Heir!',                                                                  'translated'),
		('Hello, Wife!',                                                            'Hello, Wife!',                                                                  'translated'),
		('Heroes of the Past',                                                      'Heroes of the Past',                                                            'translated'),
		('I Was Caught up in a Hero Summoning, but That World Is at Peace',         'I Was Caught up in a Hero Summoning, but That World Is at Peace',               'translated'),
		('Idle Wife, Evil Husband',                                                 'Idle Wife, Evil Husband',                                                       'translated'),
		('Immortal Pilgrimage',                                                     'Immortal Pilgrimage',                                                           'translated'),
		('Invincible Level Up',                                                     'Invincible Level Up',                                                           'translated'),
		('Kusuriya no Hitorigoto',                                                  'Kusuriya no Hitorigoto',                                                        'translated'),
		('Let Me Tease You',                                                        'Let Me Tease You',                                                              'translated'),
		('Level 1 Hero Slave',                                                      'Level 1 Hero Slave',                                                            'translated'),
		('Girl, I’ll Teach You Cultivation',                                        'Girl, I\'ll Teach You Cultivation',                                             'translated'),
		('Lone Harem Meister',                                                      'Lone Harem Meister',                                                            'translated'),
		('Marquis of Grand Xia',                                                    'Marquis of Grand Xia',                                                          'translated'),
		('Midnight Offering',                                                       'Midnight Offering',                                                             'translated'),
		('Minister Family\'s Black Belly Woman',                                    'Minister Family\'s Black Belly Woman',                                          'translated'),
		('My Entire Class Was Summoned to Another World Except for Me',             'My Entire Class Was Summoned to Another World Except for Me',                   'translated'),
		('Mystic Nan',                                                              'Mystic Nan',                                                                    'translated'),
		('Never Marry a Man With Two Tintins',                                      'Never Marry a Man With Two Tintins',                                            'translated'),
		('Official Savior',                                                         'Official Savior',                                                               'translated'),
		('On the Way Home I Got a Bride and Twin Daughters Who Were Dragons',       'On the Way Home I Got a Bride and Twin Daughters, Who Were Dragons',            'translated'),
		('On the Way Home I Got a Bride and Twin Daughters, Who Were Dragons',      'On the Way Home I Got a Bride and Twin Daughters, Who Were Dragons',            'translated'),
		('One Man’s Journey',                                                       'One Man\'s Journey',                                                            'translated'),
		('Ore no Isekai Shimai ga Jichou Shinai!',                                  'Ore no Isekai Shimai ga Jichou Shinai!',                                        'translated'),
		('Primordial Blood Throne',                                                 'Primordial Blood Throne',                                                       'translated'),
		('pygmalion',                                                               'Pygmalion Is Planting Seeds',                                                   'translated'),
		('Rebirth of an Abandoned Woman',                                           'Rebirth of an Abandoned Woman',                                                 'translated'),
		('Refusing To Serve Me? Then Off With Your Head!',                          'Refusing To Serve Me? Then Off With Your Head!',                                'translated'),
		('Refusing to Serve Me? Then Off With Your Head',                           'Refusing To Serve Me? Then Off With Your Head!',                                'translated'),
		('Revolution of the 8th Class Mage',                                        'Revolution of the 8th Class Mage',                                              'translated'),
		('She Died',                                                                'She Died',                                                                      'translated'),
		('Skirt-Chasing Young Monarch',                                             'Skirt-Chasing Young Monarch',                                                   'translated'),
		('Skirt-Chasing Young Monarch: City Lady-Killer',                           'Skirt-Chasing Young Monarch: City Lady-Killer',                                 'translated'),
		('Spring and Autumn\'s Dream',                                              'Spring and Autumn\'s Dream',                                                    'translated'),
		('Super Driver',                                                            'Super Driver',                                                                  'translated'),
		('Super Evolution',                                                         'Super Evolution',                                                               'translated'),
		('The Devil’s Evolution Catalog',                                           'The Devil’s Evolution Catalog',                                                 'translated'),
		('The General’s Little Peasant Wife',                                       'The General’s Little Peasant Wife',                                             'translated'),
		('The Harem Was a Forced Goal',                                             'The Harem Was a Forced Goal',                                                   'translated'),
		('The Last Surviving Alchemist',                                            'The Last Surviving Alchemist',                                                  'translated'),
		('The Military Female Soldier With Unwavering Stubbornness',                'The Military Female Soldier With Unwavering Stubbornness!',                     'translated'),
		('The Military Female Soldier With Unwavering Stubbornness',                'The Military Female Soldier With Unwavering Stubbornness!',                     'translated'),
		('The Returner',                                                            'The Returner',                                                                  'translated'),
		('The Royal Princess Fox',                                                  'The Royal Princess Fox',                                                        'translated'),
		('The Second Coming of Avarice',                                            'The Second Coming of Avarice',                                                  'translated'),
		('The Strange Adventure of a Broke Mercenary',                              'The Strange Adventure of a Broke Mercenary',                                    'translated'),
		('The Strongest Wingless Gargoyle',                                         'The Strongest Wingless Gargoyle',                                               'translated'),
		('The Two-Faced Venerate Emperor Give Me A Hug',                            'The Two-Faced Venerate Emperor, Give Me A Hug',                                 'translated'),
		('The Two-Faced Venerate Emperor',                                          'The Two-Faced Venerate Emperor, Give Me A Hug',                                 'translated'),
		('The Two-Faced Venerate Emperor, Give Me A Hug',                           'The Two-Faced Venerate Emperor, Give Me A Hug',                                 'translated'),
		('The Undying Drama',                                                       'The Undying Drama',                                                             'translated'),
		('The Urban Successor of God of Gluttony',                                  'The Urban Successor of God of Gluttony',                                        'translated'),
		('The Villains Need to Save the World?',                                    'The Villains Need to Save the World?',                                          'translated'),
		('The Woman Who Accepted Her Fate',                                         'The Woman Who Accepted Her Fate',                                               'translated'),
		('The Yu Brother\'s Case Book',                                             'The Yu Brother\'s Case Book',                                                   'translated'),
		('Transcending Evolution',                                                  'Transcending Evolution',                                                        'translated'),
		('Virtual Evolution',                                                       'Virtual Evolution',                                                             'translated'),
		('Age Of Worldwide Monsters',                                               'Age Of Worldwide Monsters',                                                     'translated'),
		('I Have A Manor In The Post-Apocalyptic Era',                              'I Have A Manor In The Post-Apocalyptic Era',                                    'translated'),
		('Watchmen',                                                                'Watchmen',                                                                      'translated'),
		('Womanizing Mage',                                                         'Womanizing Mage',                                                               'translated'),
		('Xian Wang Dotes On Wife',                                                 'Xian Wang Dotes On Wife',                                                       'translated'),
		('Yandere Megami No Hakoniwa',                                              'Yandere Megami No Hakoniwa',                                                    'translated'),
		('Princess and the General',                                                'Princess and the General',                                                      'translated'),
		('Yong Heng Zhi Zun',                                                       'Yong Heng Zhi Zun',                                                             'translated'),
		('Devouring Heaven Sword God',                                              'Devouring Heaven Sword God',                                                    'translated'),
		('The Magic Academy’s Romantic Circumstances',                              'The Magic Academy’s Romantic Circumstances',                                    'translated'),


		('Aeterna Saga',                                                            'Aeterna Saga',                                                                  'oel'),
		('Antagonist Rewind',                                                       'Antagonist Rewind',                                                             'oel'),
		('Black Titan',                                                             'Black Titan',                                                                   'oel'),
		('Black Watch Asylum',                                                      'Black Watch Asylum',                                                            'oel'),
		('David the Demon',                                                         'David the Demon',                                                               'oel'),
		('Divine Cruelty',                                                          'Divine Cruelty',                                                                'oel'),
		('Ethereal Heavens',                                                        'Ethereal Heavens',                                                              'oel'),
		('Fighting God',                                                            'Fighting God',                                                                  'oel'),
		('Girl, I\'ll Teach You Cultivation',                                       'Girl, I\'ll Teach You Cultivation',                                             'oel'),
		('God\'s Island',                                                           'God\'s Island',                                                                 'oel'),
		('Heathens',                                                                'Heathens',                                                                      'oel'),
		('Heavenward on Golden Wings Book 2',                                       'Heavenward on Golden Wings',                                                    'oel'),
		('Heavenward On Golden Wings',                                              'Heavenward on Golden Wings',                                                    'oel'),
		('Hidden Forge: Lucem Ac Tenebras',                                         'Hidden Forge: Lucem Ac Tenebras',                                               'oel'),
		('I Didn\'t Even Want to Live, But God Forced Me to Reincarnate',           'I Didn\'t Even Want to Live, But God Forced Me to Reincarnate',                 'oel'),
		('Indomitable Oathbreaker',                                                 'Indomitable Oathbreaker',                                                       'oel'),
		('KARMA STREAMER',                                                          'Karma Streamer',                                                                'oel'),
		('Kingdom of Lost Souls',                                                   'Kingdom of Lost Souls',                                                         'oel'),
		('Level 1 Hero Slave',                                                      'Level 1 Hero Slave',                                                            'oel'),
		('Life and Times of Mitch and Akki',                                        'Life and Times of Mitch and Akki',                                              'oel'),
		('Lord of Darkness',                                                        'Lord of Darkness',                                                              'oel'),
		('Magical Tournament',                                                      'Magical Tournament',                                                            'oel'),
		('Number One Commander',                                                    'Number One Commander',                                                          'oel'),
		('One Man\'s Journey',                                                      'One Man\'s Journey',                                                            'oel'),
		('Orphans of a Dead Nation',                                                'Orphans of a Dead Nation',                                                      'oel'),
		('Path of Blood',                                                           'Path of Blood',                                                                 'oel'),
		('Project Cypher',                                                          'Project Cypher',                                                                'oel'),
		('Red Souls',                                                               'Red Souls',                                                                     'oel'),
		('Regarding The Life of A Certain Fallen Noble',                            'Regarding The Life of A Certain Fallen Noble',                                  'oel'),
		('Solitary Sword Sovereign',                                                'Solitary Sword Sovereign',                                                      'oel'),
		('Son of the Night',                                                        'Son of the Night',                                                              'oel'),
		('The Abandoned',                                                           'The Abandoned',                                                                 'oel'),
		('The Adventures of the Mask Maker',                                        'The Adventures of the Mask Maker',                                              'oel'),
		('The Average Man',                                                         'The Average Man',                                                               'oel'),
		('The Clockwork Raven',                                                     'The Clockwork Raven',                                                           'oel'),
		('The Golden Children',                                                     'The Golden Children',                                                           'oel'),
		('The Lost Crest',                                                          'The Lost Crest',                                                                'oel'),
		('Three Lifetimes',                                                         'Three Lifetimes',                                                               'oel'),
		('threelifetimes',                                                          'Three Lifetimes',                                                               'oel'),
		('Walking With Giants',                                                     'Walking With Giants',                                                           'oel'),



		# So CR did a major rewrite for their site. For no good reason, and it fucked up the tags. 
		# Siiiiigh.
		('102',                                                                     'Beloved Empress',                                                               'translated'), 
		('110',                                                                     'Heroes of the Past',                                                            'translated'), 
		('111',                                                                     'Yandere Megami No Hakoniwa',                                                    'translated'), 
		('112',                                                                     'The Two-Faced Venerate Emperor, Give Me A Hug',                                 'translated'), 
		('117',                                                                     'The Military Female Soldier With Unwavering Stubbornness',                      'translated'), 
		('124',                                                                     'One Man\'s Journey',                                                            'translated'), 
		('127',                                                                     'Womanizing Mage',                                                               'translated'), 
		('128',                                                                     'The Villains Need to Save the World?',                                          'translated'), 
		('130',                                                                     'Hello, Wife!',                                                                  'translated'), 
		('132',                                                                     'Hello, Heir!',                                                                  'translated'), 
		('133',                                                                     'Godly Student',                                                                 'translated'), 
		('136',                                                                     'Eternal Reverence',                                                             'translated'), 
		('20979',                                                                   'Never Marry a Man with Two Tintins',                                            'translated'), 
		('24542',                                                                   'Son of the Night',                                                              'oel'), 
		('27144',                                                                   'Number One Commander',                                                          'oel'), 
		('28844',                                                                   'I Didn\'t Even Want to Live, But God Forced Me to Reincarnate!',                'oel'), 
		('32',                                                                      'Karma Streamer',                                                                'oel'), 
		('35542',                                                                   'The Second Coming of Avarice',                                                  'translated'), 
		('43830',                                                                   'Super Driver',                                                                  'translated'), 
		('45915',                                                                   'Kingdom of Lost Souls',                                                         'oel'), 
		('67',                                                                      'Ore no Isekai Shimai ga Jichou Shinai!',                                        'translated'), 
		('71',                                                                      'Invincible Level Up',                                                           'translated'), 
		('73',                                                                      'Rebirth of an Abandoned Woman',                                                 'translated'), 
		('78',                                                                      'The General\'s Little Peasant Wife',                                            'translated'), 
		('80',                                                                      'Kusuriya no Hitorigoto',                                                        'translated'), 
		('83',                                                                      'Great Han\'s Female General Wei Qiqi',                                          'translated'), 
		('91',                                                                      'Skirt-Chasing Young Monarch: City Lady-Killer',                                 'translated'), 
		('76459',                                                                   'Invincible Exchange System',                                                    'translated'), 
		('70560',                                                                    'Princess and the General',                                                     'translated'), 
		('9311',                                                                    'The Returner',                                                                  'translated'), 
		('1274',                                                                    'The Devil’s Evolution Catalog',                                                 'translated'), 
		('140',                                                                     'The Last Surviving Alchemist',                                                  'translated'), 
		('116',                                                                     'Xian Wang Dotes On Wife',                                                       'translated'), 
		('60831',                                                                   'Devouring Heaven Sword God',                                                    'translated'), 
		('80744',                                                                   'Song of Adolescence',                                                           'translated'), 
		('The Dragon Within',                                                       'The Dragon Within',                                                             'oel'),
		('42254',                                                                   'The Dragon Within',                                                             'oel'),
		('56862',                                                                   'Magikind',                                                                      'oel'),
		('Earth’s Core',                                                            'Earth\'s Core',                                                                 'oel'),
		('A Tail’s Misfortune',                                                     'A Tail\'s Misfortune',                                                          'oel'),
		('Impulsive: Descendants of the Gifted',                                    'Impulsive: Descendants of the Gifted',                                          'oel'),
		('Sky Fall Legend',                                                         'Sky Fall Legend',                                                               'oel'),
		('Nothing But Bones',                                                       'Nothing But Bones',                                                             'oel'),
		('Substitute Hero',                                                         'Substitute Hero',                                                               'oel'),
		('71838',                                                                   'Turn-Based Engineer',                                                           'oel'),
		('78094',                                                                   'Chrysalis',                                                                     'oel'),
		('62895',                                                                   'Conquer',                                                                       'oel'),
		('77749',                                                                   'A Collage of Stories',                                                          'oel'),
		('77299',                                                                   'Reborn: Apocalypse',                                                            'oel'),
		('106521',                                                                  'Tempestatem',                                                                   'oel'),
		('61891',                                                                   'The Wrold of Algratha',                                                         'oel'),
		('76674',                                                                   'Tales of the ESDF',                                                             'oel'),
		('65170',                                                                   'Re: Sword Emperor',                                                             'oel'),
		('58640',                                                                   'Impulsive: Descendants of the Gifted',                                          'oel'),
		('66420',                                                                   'The Predator',                                                                  'oel'),
		('Magikind',                                                                'Magikind',                                                                      'oel'),
		('77387',                                                                   'Endless Path : Infinite Cosmos',                                                'oel'),
		('66260',                                                                   'Death\'s Embrace',                                                              'oel'),
		('90349',                                                                   'Sword of The King',                                                             'oel'),
		('62818',                                                                   'A Tail’s Misfortune',                                                           'oel'),
		('135625',                                                                  'World Keeper',                                                                  'oel'),
		('135895',                                                                  'Slime and Punishment',                                                          'oel'),
		('127616',                                                                  'Paragon’s Fall',                                                                'oel'),
		('134956',                                                                  'Parallel – A Virtual Reality.',                                                 'oel'),
		('134593',                                                                  'ATL: Stories from the Retrofuture',                                             'oel'),
		('134620',                                                                  'S-Rank in Another World',                                                       'oel'),
		('105',                                                                     'Orphans of a Dead Nation',                                                      'oel'),
		('119957',                                                                  'The Eternal Sanctum',                                                           'oel'),
		('121263',                                                                  'Zeroth Knight',                                                                 'oel'),
		('127361',                                                                  'Qt: Against My Will',                                                           'oel'),
		('127934',                                                                  'Holy Akashic Conqueror',                                                        'oel'),
		('134283',                                                                  'The Adventures of Sherlock Holmes',                                             'oel'),
		('135625',                                                                  'World Keeper',                                                                  'oel'),
		('136301',                                                                  'The Abandoned',                                                                 'oel'),
		('138',                                                                     'Level 1 Hero Slave',                                                            'oel'),
		('78094',                                                                   'Chrysalis',                                                                     'oel'),
		('134240',                                                                  'Journey of 365 Days',                                                           'oel'),
		
		
		
		('I Didn’t Even Want to Live, But God Forced Me to Reincarnate!',           'I Didn’t Even Want to Live, But God Forced Me to Reincarnate!',                 'oel'),
		

		('78567',                      'I Woke Up Naked After Crying Myself to Sleep ~The Three Doting Dukes and The Ice Knight~',                                   'translated'),    
		('112',                        'The Two-Faced Venerate Emperor, Give Me A Hug',                                   'translated'),    
		('134',                        'Hidden Forge: Lucem Ac Tenebras',                                                 'oel'),    
		('38302',                      'Indomitable Oathbreaker',                                                         'oel'),    
		('56305',                      'Earth’s Core',                                                                    'oel'),    
		('56417',                      'Dragon’s Heart. Stone Will.',                                                     'oel'),    
		('A.I.',                       'A.I.',                                                                            'oel'),    
		('61581',                      'Substitute Hero',                                                                 'oel'),    
		('71603',                      'The Witch\'s game',                                                               'oel'),    
		('76038',                      'Ascension To The Apex',                                                           'oel'),    
		('71851',                      'Dungeon\'s Escapee',                                                              'oel'),    
		('58482',                      'A.I.',                                                                            'oel'),    
		('78355',                      'His King\'s Traveler',                                                            'oel'),    
		('86409',                      'Eye of Souls',                                                                    'oel'),    
		('88766',                      'The Oscillation',                                                                 'oel'),    
		('60455',                      'Sky Fall Legend',                                                                 'oel'),    
		('Sovereign of the Gates',     'Sovereign of the Gates',                                                          'oel'),    
		('61242',                      'Sovereign of the Gates',                                                          'oel'),    
		('70384',                      'I Have A Manor In The Post-Apocalyptic Era',                                      'translated'),    
		('73971',                      'Champion is Playing',                                                             'translated'),    
		('136557',                     'Sovereign of Blood',                                                              'oel'),
		('135015',                     'Entertainment Industry',                                                          'oel'),
		('137046',                     'Crossing the Divide',                                                             'oel'),
		('130032',                     'My Wife Spoils Me Too Much',                                                      'translated'),
		('130701',                     'Cursed Heroine',                                                                  'oel'),
		('134049',                     'Dracula',                                                                         'oel'),
		('143956',                     'Chronicles of Fate',                                                              'oel'),
		('144700',                     'Welcome to Freak Class!',                                                         'translated'),
		('140483',                     'Undying Empire',                                                                  'oel'),
		('139605',                     'The betrayal',                                                                    'oel'),
		('56681',                      'A Hero Returns',                                                                  'oel'),
		('126985',                                                                   'Final Boss',                                                                      'translated'),
		('140463',                                                                   'Emperor NPC',                                                                      'oel'),

		

	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	
	snames = [
			'Aeterna Saga', 
			'Antagonist Rewind',
			'Black Watch Asylum', 
			'Castle of Black Iron', 
			'Fighting God', 
			'Grave Robber',
			'Heavenward on Golden Wings Book 2', 
			'Heavenward On Golden Wings', 
			'Invincible Level Up', 
			'Let Me Tease You',
			'Life and Times of Mitch and Akki', "God's Island", 'Black Titan', 
			'Lone Harem Meister',
			'Lone Harem Meister',
			'Lone Harem Meister', 
			'Magical Tournament', 
			'My Entire Class Was Summoned to Another World Except for Me',
			'Mystic Nan',
			'Mystical Nan', 
			'Official Savior',
			'Orphans of a Dead Nation', 
			'Path of Blood',
			'Primordial Blood Throne',
			'Rebirth of an Abandoned Woman', 
			'Regarding The Life of A Certain Fallen Noble',
			'She Died',
			'Skirt-Chasing Young Monarch',
			'Super Insight System',
			'The Abandoned', 
			'The Adventures of the Mask Maker',
			'The Clockwork Raven', 
			'The Harem Was a Forced Goal',
			'The Royal Princess Fox',
			'The Strongest Wingless Gargoyle',
			'The Woman Who Accepted Her Fate',
			'Three Lifetimes', 
			'Transcending Evolution', 
			'Villainess', 
			'Virtual Evolution', 
			'Walking With Giants', 
	    ]
	    
	tlut = {tmp.lower(): tmp for tmp in snames}
	
	tlut['midnight offering'] = 'Midnight Offering: Hades\'s Little Pet'
	tlut['pygmalion'] = 'Pygmalion Is Planting Seeds'
	tlut['hogw chapter'] = 'Heavenward On Golden Wings'
	tlut['invincible leveling up'] = 'Level up Is Getting Me Undefeatable'
	
	ltags = [tmp.lower() for tmp in item['tags']]
	
	
	for key, value in tlut.items():
		if key in ltags:
			if '/translations/' in item['linkUrl']:
			
				tl_type = 'translated'
			elif '/originals/' in item['linkUrl']:
				tl_type = 'oel'
			else:
				# This /shouldn't/ get hit.
				return False
			return buildReleaseMessageWithType(item, value, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)
			
			
	titlemap = [
		('The Strongest Wingless Gargoyle',                                      'The Strongest Wingless Gargoyle',                               'translated'),
		('My Entire Class Was Summoned to Another World Except for Me',          'My Entire Class Was Summoned to Another World Except for Me',   'translated'),
		('The Harem Was a Forced Goal',                                          'The Harem Was a Forced Goal',                                   'translated'),
		('HoGW Chapter',                                                         'Heavenward on Golden Wings',                                    'oel'),
		('HoGW BK II',                                                           'Heavenward on Golden Wings',                                    'oel'),
		('Invincible Level Up',                                                  'Invincible Level Up',                                           'translated'),
		('Two-Faced Venerate Emperor, Give Me A Hug: Chapter ',                  'The Two-Faced Venerate Emperor',                                'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)
	
	
	if 'Dragon’s Heart. Stone Will. Book I. LitRPG wuxia series' in item['tags'] and vol is None:
		vol = 1
		return buildReleaseMessageWithType(item, 'Dragon\'s Heart', vol, chp, frag=frag, postfix=postfix, tl_type='translated')
		
	
	return False