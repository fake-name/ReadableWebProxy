def extractRebirthOnlineWorld(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
		
	# if item['tags'] == [] and item['title'].lower().startswith("chapter"):
	# 	return None
	# if item['tags'] == [] and item['title'].lower().startswith("row: chapter "):
	# 	return None
		
	# Christ, Rebirth Online World is a complete mess.

	tagmap = [
		('Jikuu Mahou TL',                'Jikuu Mahou de Isekai to Chikyuu wo Ittarikitari',                                            'translated'),
		('Isekai Shoukan',                'Isekai Shoukan Makikomu Ijousha',                                                             'translated'),
		('Magic Bullet',                  'Magic Bullet in Magic Land',                                                                  'translated'),
		('Monster Musume',                'Monster Musume Harem o Tsukurou!',                                                            'translated'),
		('Monster Musume',                'Parameter Remote Controller',                                                                 'translated'),
		('TWVUE',                         'Tales of the Wickedly Vicious Underground Empire',                                            'translated'),
		('PRC',                           'Parameter Remote Control',                                                                    'translated'),
		('TOWN',                          'The Ability to make town!? ~Let’s make a Japanese Town in Different world~',                  'translated'),
		('Ex-hero',                       'Ex-Hero Candidate’s, who turned out to be a cheat from lv2, laid-back life in Another World', 'translated'),
		('Earth Core',                    "Earth's Core",                                                                                'oel'),
		('goddess grant me a girlfriend', 'Goddess Grant me a Girlfriend',                                                               'oel'),
		('Loiterous',                     'Loiterous',                                                                                   'oel'),
		('Parallel World Mafia',          'In A Parallel World With Random Skills, I Reluctantly Become A Mafia Boss?',                  'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	urlfrag = [

		('/400-years-old-virgin-demon-king-chapter-',                         '400 Years Old Virgin Demon King',                                                             'translated'),
		('/afgitmolfm-',                                                      'AFGITMOLFM',                                                                                  'translated'),
		('/ataxias-chp-',                                                     'Ataxias - Sekai no douran',                                                                   'oel'),
		('/birth-of-a-necromancer-',                                          'Birth of a Necromancer',                                                                      'oel'),
		('/cruel-king-and-the-princess',                                      'Cruel Emperor and the Princess of Prophecy',                                                  'translated'),
		('/demon-lord-and-his-hero-chapter-',                                 'Demon Lord and His Hero',                                                                     'oel'),
		('/gods-fragment-doctrine-chapter-',                                  'God\'s Fragment: Doctrine',                                                                   'oel'),
		('/harem-of-the-dora-prince-chapter-',                                'Harem of the Dora Prince',                                                                    'oel'),
		('/hyaku-ma-no-shu-chapter-',                                         'yaku ma no Shu',                                                                              'translated'),
		('/isekai-shoukan-',                                                  'Isekai shoukan makikomu ijousha',                                                             'translated'),
		('/jintetsu-chapter-',                                                'Jintetsu',                                                                                    'oel'),
		('/last-high-human-',                                                 'Last High Human',                                                                             'oel'),
		('/legend-of-gemini-',                                                'Legend of Gemini',                                                                            'translated'),
		('/magic-bullet-chp-',                                                'Magic Bullet in Magic Land',                                                                  'translated'),
		('/minglan-',                                                         'The Legend of the Concubine’s Daughter Minglan',                                              'translated'),
		('/monster-musume-chapter-',                                          'Monster Musume Harem wo Tsukurou!',                                                           'translated'),
		('/nidome-no-yuusha-',                                                'Nidome no Yuusha',                                                                            'translated'),
		('/novel/nidome-no-yuusha/',                                          'Nidome no Yuusha',                                                                            'translated'),
		('/novel/adventures-in-another-world-onward-good-friends',            'Adventures in Another World, Onward Good Friends!!!',                                         'oel'),
		('/novel/balada',                                                     'Balada: When death did not exist, nor yet Eternity Part I',                                   'oel'),
		('/novel/black-butterfly',                                            'Black Butterfly',                                                                             'oel'),
		('/novel/but-god-forced-me-to-reincarnate',                           'I Don\'t Even Want to Live, but God Forced me to Reincarnate',                                'oel'),
		('/novel/demon-lord-and-his-hero',                                    'Demon Lord and His Hero',                                                                     'oel'),
		('/novel/dwelling-of-wild-thoughts',                                  'Dwelling of Wild Thoughts',                                                                   'oel'),
		('/novel/fantasy-school-saves-world',                                 'The School that saves the world? I have super powers!?',                                      'oel'),
		('/novel/lost-lightning-heart',                                       'Lost Lightning Heart',                                                                        'oel'),
		('/novel/other-world-assassin-life-of-a-man-who-was-a-shut-in',       'Other World Assassin Life of a Man who was a Shut-in',                                        'translated'),
		('/novel/parthios-and-yuki-fanfiction',                               'Harem of the Dora Prince',                                                                    'oel'),
		('/novel/rebirth',                                                    'Rebirth',                                                                                     'oel'),
		('/rebirth-chapter-',                                                 'Rebirth',                                                                                     'oel'),
		('/novel/the-abyss',                                                  'What would you do in the underworld\'s Abyss? Do you run, hide or is it time to roll?',       'oel'),
		('/novel/two-fish-in-a-bottle',                                       'Two Fish in A Bottle',                                                                        'translated'),
		('/other-world-assassin-life-of-a-man-who-was-a-shut-in-chapter-',    'Other World Assassin Life of a Man who was a Shut-in',                                        'translated'),
		('/otherworld-life-of-an-assassin-who-was-a-shut-in-',                'Other World Assassin Life of a Man who was a Shut-in',                                        'translated'),
		('/talisman-emperor-chapter-',                                        'Talisman Emperor',                                                                            'translated'),
		('/the-world-inside-a-dream-chapter',                                 'The World Inside a Dream',                                                                    'oel'),
		('/the-world-is-a-bit-sweet-',                                        'The World is a bit Sweet',                                                                    'translated'),
		('/novel/the-world-is-a-bit-sweet/',                                  'The World is a bit Sweet',                                                                    'translated'),
		('/to-deprive-a-deprieved-person-',                                   'To Deprive a Deprived Person',                                                                'translated'),
		('/to-deprive-a-deprived-person-chapter-',                            'To Deprive a Deprived Person',                                                                'translated'),
		('/town-chapter-',                                                    'The Ability to make town!? ~Let’s make a Japanese Town in Different world~',                  'translated'),
		('/town-chp-',                                                        'The Ability to make town!? ~Let\'s make a Japanese Town in Different world~',                 'translated'),
		('/usw-vol',                                                          'Undead Seeks Warmth',                                                                         'translated'),
		('/we-live-in-dragons-peak-chapter-',                                 'We Live in Dragon\'s Peak',                                                                   'translated'),
		('/wizard\'s-tale-ch-',                                               'Wizard\'s Tale',                                                                              'translated'),
		('/wizard\'s-tale-chapter-',                                          'Wizard\'s Tale',                                                                              'translated'),
		('/wizards-tale-',                                                    'Wizard\'s Tale',                                                                              'translated'),
		('/wizards-tale-chapter-',                                            'Wizard\'s Tale',                                                                              'translated'),
		('/world-destroying-demonic-emperor-chapter-',                        'World Destroying Demonic Emperor',                                                            'translated'),
		('/world-destroying-demonic-emperor:-chapter-',                       'World Destroying Demonic Emperor',                                                            'translated'),
		('/world-devourer-chapter-',                                          'The World Devourer',                                                                          'oel'),
		('/world-traveler-arc-',                                              'World Traveler',                                                                              'oel'),
		('/wt-arc-',                                                          'World Traveler',                                                                              'oel'),
		('rebirth.online/novel/the-tutorial-is-too-hard/',                    'The Tutorial is Too Hard',                                                                    'translated'),
		('rebirth.online/novel/the-lazy-swordmaster/',                        'The Lazy Swordmaster',                                                                        'translated'),
		('rebirth.online/novel/400-years-odl-virgin-demon-king/',             '400 Years Old Virgin Demon King',                                                             'translated'),
		('rebirth.online/novel/400-years-old-virgin-demon-king/',             '400 Years Old Virgin Demon King',                                                             'translated'),
		('rebirth.online/novel/a-fairy-tale-for-the-nephilim/',               'A Fairy Tale for the Nephilim',                                                               'oel'),
		('rebirth.online/novel/adventure-in-a-foreign-world' ,                'Adventure In A Foreign World - Legacy of The Chosen One',                                     'translated'),
		('rebirth.online/novel/afgitmolfm/',                                  'AFGITMOLFM',                                                                                  'translated'),
		('rebirth.online/novel/ataxias-sekai-no-douran/',                     'Ataxias - Sekai no douran',                                                                   'oel'),
		('rebirth.online/novel/ataxias-sekai-no-douran/',                     'Ataxias - Sekai no douran',                                                                   'oel'),
		('rebirth.online/novel/balada/',                                      'Balada: When death did not exist, nor yet Eternity Part I',                                   'oel'),
		('rebirth.online/novel/birth-of-a-necromancer/',                      'Birth of a Necromancer',                                                                      'oel'),
		('rebirth.online/novel/destination-of-crybird/',                      'Destination of Crybird',                                                                      'translated'),
		('rebirth.online/novel/earths-core' ,                                 "Earth's Core",                                                                                'oel'),
		('rebirth.online/novel/ex-hero' ,                                     'Ex-Hero Candidate’s, who turned out to be a cheat from lv2, laid-back life in Another World', 'translated'),
		('rebirth.online/novel/god-fragment-doctrine/',                       'God\'s Fragment: Doctrine',                                                                   'oel'),
		('rebirth.online/novel/how-to-survive-a-summoning-101' ,              'How to Survive a Summoning 101',                                                              'oel'),
		('rebirth.online/novel/how-to-survive-a-summoning-101/',              'How to Survive a Summoning 101',                                                              'oel'),
		('rebirth.online/novel/hyaku-ma-no-shu/',                             'Hyaku ma no Shu',                                                                             'translated'),
		('rebirth.online/novel/i-became-a-hero-in-a-pandemic' ,               'I became a hero in a pandemic',                                                               'translated'),
		('rebirth.online/novel/immortal-god-emperor/',                        'Immortal God Emperor',                                                                        'translated'),
		('rebirth.online/novel/inma-no-hado' ,                                'Inma no Hado',                                                                                'translated'),
		('rebirth.online/novel/isekai-ryouridou/',                            'Isekai Ryouridou',                                                                            'translated'),
		('rebirth.online/novel/isekai-shoukan-makikomu-ijousha' ,             'Isekai shoukan makikomu ijousha',                                                             'translated'),
		('rebirth.online/novel/jikuu-mahou' ,                                 'Jikuu Mahou de Isekai to Chikyuu wo Ittarikitari',                                            'translated'),
		('rebirth.online/novel/jintetsu/',                                    'Jintetsu',                                                                                    'oel'),
		('rebirth.online/novel/jintetsu/',                                    'Jintetsu',                                                                                    'translated'),
		('rebirth.online/novel/last-high-human/',                             'Last High Human',                                                                             'oel'),
		('rebirth.online/novel/legend-of-gemini' ,                            'Legend of Gemini',                                                                            'translated'),
		('rebirth.online/novel/loiterous' ,                                   'Loiterous',                                                                                   'oel'),
		('rebirth.online/novel/loli-vampire' ,                                'When I woke up in the morning I became a silver haired loli vampire',                         'translated'),
		('rebirth.online/novel/love-parameter' ,                              'Love Parameter',                                                                              'translated'),
		('rebirth.online/novel/magic-bullet-in-magic-land' ,                  'Magic Bullet in Magic Land',                                                                  'translated'),
		('rebirth.online/novel/magic-bullet-in-magic-land/',                  'Magic Bullet in Magic Land',                                                                  'translated'),
		('rebirth.online/novel/master-of-dungeon' ,                           'Master of Dungeon',                                                                           'oel'),
		('rebirth.online/novel/monster-musume' ,                              'Monster Musume',                                                                              'translated'),
		('rebirth.online/novel/my-annoying-aura' ,                            'My Annoying Aura Follows Me Into Another World',                                              'oel'),
		('rebirth.online/novel/my-god-like-adventure/',                       'My God-like Adventure in Another World',                                                      'oel'),
		('rebirth.online/novel/second-saga' ,                                 'Second Saga',                                                                                 'oel'),
		('rebirth.online/novel/sefiria' ,                                     'Prodigy Sefiria’s Program to Overthrow the Higher Ranks',                                     'translated'),
		('rebirth.online/novel/tales-of-the-wickedly' ,                       'Tales of the Wickedly Vicious Underground Empire',                                            'oel'),
		('rebirth.online/novel/the-ability-to-make-town' ,                    'The Ability to make town!? ~Let’s make a Japanese Town in Different world~',                  'oel'),
		('rebirth.online/novel/the-lazy-dragon/',                             'The Lazy Dragon is Working Hard',                                                             'translated'),
		('rebirth.online/novel/the-legend-of-concubine-daughter-minglan/',    'The Legend of the Concubine’s Daughter Minglan',                                              'translated'),
		('rebirth.online/novel/to-deprive-a-deprived-person' ,                'To Deprive a Deprived Person',                                                                'translated'),
		('rebirth.online/novel/undead-seeks-warmth' ,                         'Undead Seeks Warmth',                                                                         'translated'),
		('rebirth.online/novel/unmotivated-hero-tale/',                       'Unmotivated Hero\'s Tale',                                                                    'translated'),
		('rebirth.online/novel/werewolf/',                                    'Werewolf Reincarnation, Aide of Demon King',                                                  'translated'),
		('rebirth.online/novel/wizard\'s-tale',                               'Wizard\'s Tale',                                                                              'translated'),
		('rebirth.online/novel/world-destroying-demonic-emperor/',            'World Destroying Demonic Emperor',                                                            'oel'),
		('rebirth.online/novel/world-devourer/',                              'The World Devourer',                                                                          'oel'),
		('rebirth.online/novel/world-devourer/',                              'The World Devourer',                                                                          'oel'),            
		('rebirth.online/novel/world-traveler' ,                              'World Traveler ',                                                                             'oel'),
		('rebirth.online/novel/yuusha-isagi-no-maou-hanashi' ,                'Yuusha Isagi no Maou Hanashi',                                                                'translated'),
		('rebirth.online/novel/yuusha-isagi-no-maou-hanashi/',                'Yuusha Isagi no Maou Hanashi',                                                                'translated'),
		('rebirth.online/novel/the-good-for-nothing-seventh-young-lady/',     'The Good for Nothing Seventh Young Lady',                                                     'translated'),
		('rebirth.online/novel/the-world-inside-a-dream/',                    'The World Inside a Dream',                                                                    'oel'),
		('rebirth.online/novel/earths-core' ,                                 "Earth's Core",                                                                                'oel'),

		('/konjiki-no-moji-tsukai-chapter-',                                  'Konjiki no Word Master',                                                                      'translated'),
		('www.rebirth.online/novel/divine-genius-healer-abandoned-woman/',    'Divine Genius Healer, Abandoned Woman: Demonic Tyrant in Love with a Mad Little Consort',     'translated'),


		# Short circult some of the one-shot cruft
		('rebirth.online/novel/madmana-original-works/',          None, None),
		('rebirth.online/novel/parthios-and-yuki-fanfiction/',    None, None),
		
		# Reviews are not goddamn "novel"s
		('rebirth.online/novel/zhaernon-review-corner',           None, None),

		# Appear to now be 404-ed
		('rebirth.online/novel/my-god-like-adventure/',           None, None),
		('rebirth.online/novel/rebirth-online/',                  None, None),
		('rebirth.online/novel/the-cooking-master/',              None, None),
		('rebirth.online/novel/future-demon/',                    None, None),
		('rebirth.online/novel/dream-clinic/',                    None, None),
		('rebirth.online/novel/boring-reincarnation/',            None, None),
		('/hero-pandemic-chapter-',                               None, None),

		
	]

	for key, name, tl_type in urlfrag:
		if key in item['linkUrl'].lower():
			if name is None:
				return None
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	titlemap = [
		('[Second Saga] Chapter',                                                                               '[Second Saga]',                                                                              'oel'), 
		('Black Jade Tiger - Chapter ',                                                                         'Black Jade Tiger',                                                                           'oel'), 
		('Destination of Crybird',                                                                              'Destination of Crybird',                                                                     'translated'), 
		('Immortal God Emperor',                                                                                'Immortal God Emperor',                                                                       'translated'), 
		('Inma no Hado chapter',                                                                                'Inma no Hado',                                                                               'translated'), 
		('Isekai Ryouridou',                                                                                    'Isekai Ryouridou',                                                                           'translated'), 
		('Lazy Dragon',                                                                                         'Taidana Doragon wa Hatarakimono',                                                            'translated'), 
		('Legged mimic chapter ',                                                                               'Legged Mimic',                                                                               'translated'), 
		('Master of Dungeon',                                                                                   'Master of Dungeon',                                                                          'oel'), 
		('Neta Chara',                                                                                          'Neta Chara',                                                                                 'translated'), 
		('Not a Fairy Tale - Chapter ',                                                                         'Not a Fairy Tale',                                                                           'oel'), 
		('Polymath Redux ',                                                                                     'Polymath Redux',                                                                             'oel'), 
		('ROW:  TGFNSYL',                                                                                       'The Good for Nothing Seventh Young Lady',                                                    'translated'), 
		('ROW: 400 years old demon king chapter',                                                               '400 Years Old Virgin Demon King',                                                            'translated'), 
		('ROW: Abyss',                                                                                          'What would you do in the underworld\'s Abyss? Do you run, hide or is it time to roll?',      'oel'), 
		('ROW: AFGITMOLFM',                                                                                     'AFGITMOLFM',                                                                                 'translated'), 
		('ROW: Ataxias - Chapter',                                                                              'Ataxias - Sekai no douran',                                                                  'oel'), 
		('ROW: Ataxias - Chp',                                                                                  'Ataxias - Sekai no douran',                                                                  'oel'), 
		('ROW: BJT ',                                                                                           'I Chose To Fake My Death',                                                                   'oel'), 
		('ROW: But God Forced me to Reincarnate',                                                               'I Don\'t Even Want to Live, but God Forced me to Reincarnate',                               'oel'), 
		('ROW: DGHAW ',                                                                                         'Divine Genius Healer, Abandoned Woman: Demonic Tyrant in Love with a Mad Little Consort',    'translated'), 
		('ROW: DGHAW Chapter',                                                                                  'Divine Genius Healer, Abandoned Woman: Demonic Tyrant in Love with a Mad Little Consort',    'translated'), 
		('ROW: Earth\'s Core',                                                                                  'Earth\'s Core',                                                                              'oel'), 
		('ROW: God\'s Fragment Doctrine',                                                                       'God\'s Fragment Doctrine',                                                                   'oel'), 
		('ROW: I Chose To Fake My Death ',                                                                      'I Chose To Fake My Death',                                                                   'oel'), 
		('ROW: I Don\'t Even Want to Live, but God Forced me to Reincarnate',                                   'I Don\'t Even Want to Live, but God Forced me to Reincarnate',                               'oel'), 
		('ROW: Jikuu Mahou',                                                                                    'Jikuu Mahou de Isekai to Chikyuu wo Ittarikitari',                                           'translated'),
		('ROW: Jikuu',                                                                                          'Jikuu Mahou de Isekai to Chikyuu wo Ittarikitari',                                           'translated'),
		('ROW: Konjiki no Moji Tsukai',                                                                         'Konjiki no Moji Tsukai',                                                                     'translated'), 
		('ROW: Legend of Gemini Chapter',                                                                       'Legend of Gemini',                                                                           'translated'), 
		('ROW: LHH',                                                                                            'Last High Human',                                                                            'oel'), 
		('ROW: Magic Bullet chapter',                                                                           'Magic Bullet',                                                                               'translated'), 
		('ROW: Marielle Clarac\'s Engagement chapter ',                                                         'Marielle Clarac\'s Engagement',                                                              'oel'), 
		('ROW: MM chapter',                                                                                     'Monster Musume',                                                                             'translated'), 
		('ROW: Not a Fairy Tale - ',                                                                            'Not a Fairy Tale',                                                                           'oel'), 
		('ROW: Project: New School!',                                                                           'Project: New School!',                                                                       'oel'), 
		('ROW: Project:New School!',                                                                            'Project: New School!',                                                                       'oel'), 
		('ROW: TGFNSYL',                                                                                        'The Good for Nothing Seventh Young Lady',                                                    'translated'), 
		('ROW: The Legend Of Minglan',                                                                          'The Legend of the Concubine’s Daughter Minglan',                                             'translated'),
		('ROW: The World Devourer',                                                                             'The World Devourer',                                                                         'oel'), 
		('ROW: The World Inside a Dream',                                                                       'The World Inside a Dream',                                                                   'oel'), 
		('ROW: TWBB ',                                                                                          'The Wolven Blade and the Bells',                                                             'oel'), 
		('ROW: Undead Seeks Warmth',                                                                            'Undead Seeks Warmth',                                                                        'translated'), 
		('ROW: Unmotivated Hero\'s Tale',                                                                       'Unmotivated Hero\'s Tale',                                                                   'translated'), 
		('ROW: WDDE: Chapter',                                                                                  'World Destroying Demonic Emperor',                                                           'translated'), 
		('ROW: What would you do in the underworld\'s Abyss? Do you run, hide or is it time to roll?',          'What would you do in the underworld\'s Abyss? Do you run, hide or is it time to roll?',      'oel'), 
		('ROW: Wizard\'s Tale Chapter',                                                                         'Wizard\'s Tale',                                                                             'translated'), 
		('ROW: World Devourer',                                                                                 'The World Devourer',                                                                         'oel'), 
		('Sefi chap',                                                                                           'Sefiria',                                                                                    'translated'), 
		('Sefiria chap',                                                                                        'Sefiria',                                                                                    'translated'), 
		('Tensei Shoujo no Rirekisho',                                                                          'Tensei Shoujo no Rirekisho',                                                                 'translated'), 
		('In The Dragon Ball Universe With The Summoning System - Chapter ',                                    'In The Dragon Ball Universe With The Summoning System',                                      'oel'), 
		('The Falcon Immortal',                                                                                 'The Falcon Immortal',                                                                        'oel'), 
		('The Last Guild',                                                                                      'The Last Guild: Remastered',                                                                 'oel'), 
		('The Wolven Blade and the Bells',                                                                      'The Wolven Blade and the Bells',                                                             'oel'), 
		('ROW: Sky Nova Ch.',                                                                                   'Sky Nova',                                                                                   'oel'), 
		('ROW: Upside Down',                                                                                    'Upside Down',                                                                                'oel'), 
		('TRTS(The Rude Time Stopper)',                                                                         'The Rude Time Stopper',                                                                      'oel'), 
		('ROW: I\'m The Heroine, But I Want to Hand That Role Over Chapter ',                                   'I\'m The Heroine, But I Want to Hand That Role Over',                                        'translated'), 
		('Werewolf chapter',                                                                                    'Werewolf',                                                                                   'translated'), 
		('The Magnificent Battle Records of A Former Noble Lady - Chapter ',                                    'The Magnificent Battle Records of A Former Noble Lady',                                      'translated'), 
		('Zombie master',                                                                                       'Zombie Master',                                                                              'translated'), 
		('ROW: When TS HS Boys Are Too Adaptable ',                                                             'When TS high school boys are too adaptable',                                                 'translated'), 
		('Pampered Consort of the Fragrant Orchard - Chapter ',                                                 'Pampered Consort of the Fragrant Orchard',                                                   'translated'), 
		('ROW: Pampered Consort of the Fragrant Orchard Chapter ',                                              'Pampered Consort of the Fragrant Orchard',                                                   'translated'), 
		('ROW: Town ch.',                                                                                       'The ability to make a Town',                                                                 'translated'), 
		('ROW: The ability to make a Town chapter ',                                                            'The ability to make a Town',                                                                 'translated'), 
		('ROW: TIMMBF ch.',                                                                                     'The Illegitimate Miss Must Be Fierce',                                                       'translated'), 
		('ROW: Hero blessed ',                                                                                  'Hero blessed by his nemesis, the largest human traitor!?',                                   'translated'), 
		('Hero blessed by his nemesis, the largest human traitor!? - Chapter ',                                 'Hero blessed by his nemesis, the largest human traitor!?',                                   'translated'), 
		('ROW: Divine Healer ch.',                                                                              'Divine Genius Healer, Abandoned Woman: Demonic Tyrant in Love with a Mad Little Consort',    'translated'), 
	]                

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	if 'tdadp' in item['title'].lower() or 'To deprive a deprived person episode'.lower() in item['title'].lower():
		if vol and chp:
			vol = None
		return buildReleaseMessageWithType(item, 'To Deprive a Deprived Person', vol, chp, frag=frag, postfix=postfix)

	if item['title'].startswith('[SS] '):
		return buildReleaseMessageWithType(item, '[Second Saga]', vol, chp, frag=frag, postfix=postfix, tl_type='oel')

	return False