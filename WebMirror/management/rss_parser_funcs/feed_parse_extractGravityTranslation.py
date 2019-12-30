def extractGravityTranslation(item):
	"""
	# Gravity Translation
	also
	# Gravity Tales
	# GravityTales

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	
	if 'gravitytales.com/post/the-kings-avatar-manhua/' in item['linkUrl']:
		return None
	
	urlfrag = [
		('gravitytales.com/post/earths-core/',                              'Earth\'s Core',                                  'oel'),
		('gravitytales.com/post/the-divine-element/',                       'The Divine Elements',                            'oel'),
		('gravitytales.com/post/rebirth-of-the-heavenly-demon/',            'Rebirth of the Heavenly Demon',                  'translated'),
		('gravitytales.com/post/ghost-blows-out-the-light/',                'Ghost Blows Out the Light',                      'translated'),
		('gravitytales.com/post/demons-diary/',                             'Demon\'s Diary',                                 'translated'),
		('gravitytales.com/post/shuras-wrath/',                             'Shura\'s Wrath',                                 'translated'),
		('gravitytales.com/post/peerless-battle-spirit/',                   'Peerless Battle Spirit',                         'translated'),
		('gravitytales.com/post/dragons-soul/',                             'Dragon\'s Soul',                                 'translated'),
		('gravitytales.com/post/ia/',                                       'Infinity Armament',                              'translated'),
		('gravitytales.com/post/aethernea/',                                'Aethernea',                                      'oel'),
		('gravitytales.com/post/apocalypse-summoner/',                      'Apocalypse Summoner',                            'translated'),
		('gravitytales.com/post/dungeon-hunter/',                           'Dungeon Hunter',                                 'translated'),
		('gravitytales.com/post/overthrowing-fate/',                        'Overthrowing Fate',                              'oel'),
		('gravitytales.com/post/chronicles-of-gu-hai/',                     'Chronicles of Gu Hai',                           'translated'),
		('gravitytales.com/post/a-dragons-curiosity/',                      'A Dragon\'s Curiosity',                          'translated'),
		('gravitytales.com/post/the-good-student/',                         'The Good Student',                               'oel'),
		('gravitytales.com/post/martial-void-king/',                        'Martial Void King',                              'oel'),
		
		('gravitytales.com/post/beauty-and-the-bodyguard/',                 'Beauty and the Bodyguard',                       'translated'),
		('gravitytales.com/post/castle-of-black-iron/',                     'Castle of Black Iron',                           'translated'),
		('gravitytales.com/post/dimensional-sovereign/',                    'Dimensional Sovereign',                          'translated'),
		('gravitytales.com/post/epoch-of-twilight/',                        'Epoch of Twilight',                              'translated'),
		('gravitytales.com/post/forty-millenniums-of-cultivation/',         'Forty Millenniums of Cultivation',               'translated'),
		('gravitytales.com/post/how-to-avoid-death-on-a-daily-basis/',      'How to Avoid Death on a Daily Basis',            'oel'),
		('gravitytales.com/post/i-am-supreme/',                             'I Am Supreme',                                   'translated'),
		('gravitytales.com/post/immortal-mortal/',                          'Immortal Mortal',                                'translated'),
		('gravitytales.com/post/library-of-heavens-path/',                  'Library of Heaven\'s Path',                      'translated'),
		('gravitytales.com/post/mmorpg-rebirth-of-the-legendary-guardian/', 'MMORPG: Rebirth of the Legendary Guardian',      'translated'),
		('gravitytales.com/post/shen-yin-wang-zuo/',                        'Shen Yin Wang Zuo',                              'translated'),
		('gravitytales.com/post/strongest-abandoned-son/',                  'Strongest Abandoned Son',                        'translated'),
		('gravitytales.com/post/the-avalon-of-five-elements/',              'The Avalon Of Five Elements',                    'translated'),
		('gravitytales.com/post/versatile-mage/',                           'Versatile Mage',                                 'translated'),
		('gravitytales.com/post/war-sovereign-soaring-the-heavens/',        'War Sovereign Soaring the Heavens',              'translated'),
		('gravitytales.com/post/way-of-choices/',                           'Way of Choices',                                 'translated'),
		('gravitytales.com/post/godly-model-creator/',                      'Godly Model Creator',                            'translated'),
		('gravitytales.com/post/a-mercenarys-war/',                         'A Mercenary\'s War',                             'translated'),
		('gravitytales.com/post/master-of-the-stars/',                      'Master of the Stars',                            'translated'),
		('gravitytales.com/post/eternal-martial-sovereign/',                'Eternal Martial Sovereign',                      'translated'),
		('gravitytales.com/post/reincarnation-of-the-strongest-sword-god/', 'Reincarnation Of The Strongest Sword God',       'translated'),
		
		('gravitytales.com/post/the-kings-avatar/',                         'The King\'s Avatar',                             'translated'),
		('gravitytales.com/post/the-black-card/',                           'The Black Card',                                 'translated'),
		('gravitytales.com/post/returning-from-the-immortal-world/',        'Returning from the Immortal World',              'translated'),
		('gravitytales.com/post/seeking-the-flying-sword-path',             'Seeking the Flying Sword Path',                  'translated'),
		('gravitytales.com/novel/hardcore-qi-worlds/',                      'Hardcore: Qi Worlds',                            'oel'),
		('gravitytales.com/post/era-of-disaster/',                          'Era of Disaster',                                'translated'),
		('gravitytales.com/post/hardcore-qi-worlds/',                       'Era of Disaster',                                'translated'),
		("gravitytales.com/post/shrouding-the-heavens/",                    "Shrouding the Heavens",                          'translated'),
		("gravitytales.com/post/the-world-online/",                         "The World Online",                               'translated'),
		
		("gravitytales.com/post/atypical-reincarnation/",                   "Atypical Reincarnation",                          'translated'),
		("gravitytales.com/post/phoenix-destiny/",                          "Phoenix Destiny",                                 'translated'),
		("gravitytales.com/post/chaotic-sword-god/",                        "Chapter Sword God",                               'translated'),
		("gravitytales.com/post/everlasting-immortal-firmament/",           "Everlasting Immortal Firmament",                  'translated'),
		("gravitytales.com/post/leveling-up-and-becoming-undefeatable/",    "Leveling Up And Becoming Undefeatable",           'translated'),
		("gravitytales.com/post/immortal-and-martial-dual-cultivation/",    "Immortal and Martial Dual Cultivation",           'translated'),
		("gravitytales.com/post/the-records-of-the-human-emperor/",         "The Human Emperor",                               'translated'),
		("gravitytales.com/post/king-of-gods/",                             "King of Gods",                                    'translated'),
		("gravitytales.com/post/rise-of-humanity/",                         "Rise of Humanity",                                'translated'),
		("gravitytales.com/post/age-of-adepts/",                            "Age of Adepts",                                   'translated'),
		("gravitytales.com/post/hidden-assassin/",                          "Hidden Assassin",                                 'translated'),
		
		
		('gravitytales.com/post/the-new-world/',                            'The New World',                                   'oel'),
		('gravitytales.com/post/spirit-hunters-of-maoshan-sect/',           'Spirit Hunters of Maoshan Sect',                  'translated'),
		('gravitytales.com/post/golden-time/',                              'Golden Time',                                     'translated'),
		('gravitytales.com/post/rise-of-the-wasteland/',                    'Rise of the Wasteland',                           'translated'),
		('gravitytales.com/post/abyss-domination/',                         'Abyss Domination',                                'translated'),
		('gravitytales.com/post/the-lords-empire/',                         'The Lord\'s Empire Chapter',                      'translated'),
		('gravitytales.com/post/ace-of-ace/',                               'Ace of Ace',                                      'translated'),
		('gravitytales.com/post/virtual-world-close-combat-mage/',          'Virtual World: Close Combat Mage',                'translated'),
		('gravitytales.com/post/legend-of-legends/',                        'Legend of Legends',                               'translated'),
		('gravitytales.com/post/the-first-hunter/',                         'The First Hunter',                                'translated'),
		('gravitytales.com/post/so-pure-so-flirtatious/',                   'So Pure, So Flirtatious',                         'translated'),
		('gravitytales.com/post/the-city-of-terror/',                       'The City of Terror',                              'translated'),
		('gravitytales.com/post/apocalypse-hunter/',                        'Apocalypse Hunter',                               'translated'),
		('gravitytales.com/post/a-war-between-spies/',                      'A War Between Spie',                              'translated'),
	]

	linklower = item['linkUrl'].lower()
	for key, name, tl_type in urlfrag:
		if key in linklower:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	
	ltags = [tmp.lower().replace('’', "'") for tmp in item['tags']]
	

	tagmap = [
		('zhan long',                                     'Zhan Long',                                     'translated'),
		('quan zhi gao shou',                             'Quan Zhi Gao Shou',                             'translated'),
		('battle through the heavens',                    'Battle Through the Heavens',                    'translated'),
		('chaotic sword god',                             'Chaotic Sword God',                             'translated'),
		('true martial world',                            'True Martial World',                            'translated'),
		('wu dong qian kun',                              'Wu Dong Qian Kun',                              'translated'),
		("demon's diary",                                 "Demon's Diary",                                 'translated'),
		('blue phoenix',                                  'Blue Phoenix',                                  'oel'),
		("the ancient's son",                             "The Ancient's Son",                             'oel'),
		('mo tian ji',                                    'Mo Tian Ji',                                    'translated'),
		('great demon king',                              'Great Demon King',                              'translated'),
		('heavenly star',                                 'Heavenly Star',                                 'translated'),
		('conquest',                                      'Conquest',                                      'translated'),
		('shadow rogue',                                  'Shadow Rogue',                                  'translated'),
		('terror paradise',                               'Terror Paradise',                               'translated'),
		('the divine elements',                           'The Divine Elements',                           'oel'),
		('the divine element',                            'The Divine Elements',                           'oel'),
		('cult of the sacred runes',                      'Cult of the Sacred Runes',                      'translated'),
		("a record of a mortal's journey to immortality", "A Record of a Mortal's Journey to Immortality", 'translated'),
		('ancient godly monarch',                         'Ancient Godly Monarch',                         'translated'),
		("i'm really a superstar",                        "I'm Really a Superstar",                        'translated'),
		('chaotic lightning cultivation',                 'Chaotic Lightning Cultivation',                 'translated'),
		("the king's avatar",                             "The King's Avatar",                             'translated'),
		('ze tian ji',                                    'Ze Tian Ji',                                    'translated'),
		('way of choices',                                'Ze Tian Ji',                                    'translated'),
		('str',                                           'Sovereign of the Three Realms',                 'translated'),
		('dimensional sovereign',                         'Dimensional Sovereign',                         'translated'),
		('dungeon hunter',                                'Dungeon Hunter',                                'translated'),
		('king of gods',                                  'King of Gods',                                  'translated'),
		('overthrowing fate',                             'Overthrowing Fate',                             'translated'),
		('paradise of the demons and gods',               'Paradise of the Demons and Gods',               'translated'),
		('reincarnator',                                  'Reincarnator',                                  'translated'),
		('the experimental log of the crazy lich',        'The Experimental Log of the Crazy Lich',        'translated'),
		('king of gods',                                  'King of Gods',                                  'translated'),
		('martial world',                                 'Martial World',                                 'translated'),
		('rmji',                                          "A Record of A Mortal's Journey to Immortality", 'translated'),
		('the nine cauldrons',                            'The Nine Cauldrons',                            'translated'),
		('the trembling world',                           'The Trembling World',                           'translated'),
		('ancient strengthening technique',               'Ancient Strengthening Technique',               'translated'),
		('nine heavenly thunder manual',                  'Nine Heavenly Thunder Manual',                  'translated'),
		('the beginning after the end',                   'The Beginning After the End',                   'oel'),
		("a dragon's curiosity",                          "A Dragon's Curiosity",                          'oel'),
	]
	

	for tagname, name, tl_type in tagmap:
		if tagname in ltags:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	titlemap = [
		('The King’s Avatar Chapter ',     "The King's Avatar",                'translated'),
		('Against Heaven :',               'Against Heaven',                   'translated'),
		('Great Demon King',               'Great Demon King',                 'translated'),
		('Ascension of The Alchemist God', 'Ascension of the Alchemist God',   'translated'),
		('TAG Chapter',                    'Ascension of the Alchemist God',   'translated'),
		('The Alchemist God: Chapter',     'Ascension of the Alchemist God',   'translated'),
		('Might of the Stars',             'Might of the Stars',               'oel'),
		('Conquest Chapter',               'Conquest',                         'translated'),
		('Blood Hourglass',                'Blood Hourglass',                  'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



	titlestart = [
		('zhan long chapter ',                                              'Zhan Long',                                                                         'translated'),
		('a dragon’s curiosity chapter',                                    'A Dragon’s Curiosity',                                                              'translated'),
		('a record of a mortal’s journey to immortality – chapter',         "A Record of A Mortal's Journey to Immortality",                                     'translated'),
		('ancient strengthening technique: chapter',                        'Ancient Strengthening Technique',                                                   'translated'),
		('blue phoenix chapter',                                            'Blue Phoenix',                                                                      'oel'),
		('blue phoenix – chapter',                                          'Blue Phoenix',                                                                      'oel'),
		('btth ',                                                           'Battle Through the Heavens',                                                        'translated'),
		('chaotic lightning cultivation chapter',                           'Chaotic Lightning Cultivation',                                                     'translated'),
		('chaotic sword god chapter',                                       'Chaotic Sword God',                                                                 'translated'),
		('cult of the sacred runes',                                        'Cult of the Sacred Runes',                                                          'translated'),
		('earth\'s core book',                                              "Earth's Core",                                                                      'oel'),
		('era of shamans chapter',                                          'Era of Shamans',                                                                    'translated'),
		('hedonist sovereign chapter',                                      'Hedonist Sovereign',                                                                'translated'),
		('htaddb chapter',                                                  'How To Avoid Death On A Daily Basis',                                               'oel'),
		('imdc chapter',                                                    'Immortal and Martial Dual Cultivation',                                             'translated'),
		('iras',                                                            'I’m Really a Superstar',                                                            'translated'),
		('i’m really a superstar chapter',                                  "I'm Really a Superstar",                                                            'translated'),
		('jiu shen chapter',                                                'Jiu Shen',                                                                          'translated'),
		('king of gods chapter ',                                           'King of Gods',                                                                      'translated'),
		('king of gods – ',                                                 'King of Gods',                                                                      'translated'),
		('lord xue ying chapters',                                          'Lord Xue Ying',                                                                     'translated'),
		('martial world chapter',                                           'Martial World',                                                                     'translated'),
		('master of the stars chapter',                                     'Master of the Stars',                                                               'translated'),
		('mw chapter',                                                      'Martial World',                                                                     'translated'),
		('nine heavenly thunder manual chapter',                            'Nine Heavenly Thunder Manual',                                                      'translated'),
		('paradise of the demons and gods ',                                'Paradise of the Demons and Gods',                                                   'translated'),
		('paradise of the demons and gods chapter',                         'Paradise of the Demons and Gods',                                                   'translated'),
		('qzgs ',                                                           'Quan Zhi Gao Shou',                                                                 'translated'),
		('reincarnator',                                                    'Reincarnator',                                                                      'translated'),
		('rmji ',                                                           "A Record of a Mortal's Journey to Immortality",                                     'translated'),
		('shura\'s wrath chapter ',                                         'Shura\'s Wrath',                                                                    'translated'),
		('the beginning after the end',                                     'The Beginning After the End',                                                       'oel'),
		('the experimental log of the crazy lich chapter',                  'The Experimental Log of the Crazy Lich',                                            'translated'),
		('the king\'s avatar chapter',                                      'The King\'s Avatar',                                                                'translated'),
		('the king’s avatar (qzgs)',                                        "The King's Avatar",                                                                 'translated'),
		('the nine cauldrons book',                                         'The Nine Cauldrons',                                                                'translated'),
		('the nine cauldrons chapter',                                      'The Nine Cauldrons',                                                                'translated'),
		('the trembling world chapter ',                                    'The Trembling World',                                                               'translated'),
		('tka chapter ',                                                    "The King's Avatar",                                                                 'translated'),
		('true martial world chapter',                                      'True Martial World',                                                                'translated'),
		('zl ',                                                             'Zhan Long',                                                                         'translated'),
		('ztj chapter',                                                     'Ze Tian Ji',                                                                        'translated'),
		('apocalypse hunter chapter ',                                      'Apocalypse Hunter',                                                                 'translated'),
	]


	ltitle = item['title'].lower()
	for titlecomponent, name, tl_type in titlestart:
		if ltitle.startswith(titlecomponent):
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



	if item['title'].startswith('RMJI') and 'Release' in item['title']:
		return buildReleaseMessageWithType(item, "A Record of A Mortal's Journey to Immortality", vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)
		

		
	return False