def extractWordexcerptCom(item):
	'''
	Parser for 'wordexcerpt.com'
	'''

	if "teaser" in item['title'].lower():
		return None
		
	procn = item['linkUrl'].replace("-", " ").replace("/", " ") + " " + item['title']
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(procn)
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
	

	tagmap = [
		#('InfiniteResistance',        'Infinite Resistance',                      'translated'),
		#('Infinite Resistance',       'Infinite Resistance',                      'translated'),
		#('Supreme God',               'Supreme God',                              'translated'),
		('Lady\'s Sickly Husband',                               'Lady\'s Sickly Husband',                                                           'translated'),
		('Golden Age of Phoenix',                                'Golden Age of Phoenix',                                                            'translated'),
		('Real Cheat Online',                                    'Real Cheat Online',                                                                'translated'),
		('Seirei Gensouki: Konna Sekai De Deaeta Kimi Ni',       'Seirei Gensouki: Konna Sekai De Deaeta Kimi Ni',                                   'translated'),
		('Seirei Gensouki',                                      'Seirei Gensouki: Konna Sekai De Deaeta Kimi Ni',                                   'translated'),
		('Rebirth of the Tyrant: Regent Prince Is Too Fierce',   'Rebirth of the Tyrant: Regent Prince Is Too Fierce',                               'translated'),
		('Rebirth of the Tyrant',                                'Rebirth of the Tyrant',                                                            'translated'),
		('Perfect Era',                                          'Perfect Era',                                                                      'translated'),
		('Parasite',                                             'Parasite',                                                                         'translated'),
		('Emperor\'s Might',                                     'Emperor\'s Might',                                                                 'translated'),
		('Ankoku Kishi Monogatari',                              'Ankoku Kishi Monogatari',                                                          'translated'),
		('Behemoth\'s Pet',                                      'Behemoth\'s Pet',                                                                  'translated'),
		('Rebirth of the Tyrant\'s Pet',                         'Rebirth of the Tyrant\'s Pet',                                                     'translated'),
		('(WN) Seirei Gensouki',                                 'Seirei Gensouki',                                                                  'translated'),
		('Behemoth’s Pet',                                       'Behemoth\'s Pet',                                                                  'translated'),  
		('Raising a Supporting Male Lead',                       'Guide to Raising a Supporting Male Lead',                                          'translated'),  
		('Heroes of Marvel',                                     'Heroes of Marvel',                                                                 'translated'),  
		('Number 1. Ideal Witch',                                'Second Story Online: Aiming To Become The World\'s Number 1. Ideal Witch',         'translated'),  
		('Supreme God',                                          'Supreme God',                                                                      'translated'),  
		('King Arthur',                                          'My Wife, King Arthur',                                                             'translated'),  
		('My Wife, King Arthur',                                 'My Wife, King Arthur',                                                             'translated'),  
		('I Refuse to be a Supporting Character',                'I Refuse to be a Supporting Character',                                            'translated'),  
		('Last Day On Earth',                                    'Last Days On Earth',                                                               'translated'),  
		('Refuse to be a Supporting Character',                  'I Refuse to be a Supporting Character',                                            'translated'),  
		('Quick Transmigration',                                 'Quick Transmigration: Fate Trading System',                                        'translated'),  
		('History\'s Strongest Husband',                         'History\'s Strongest Husband',                                                     'translated'),  
		('Witch Rebirth: STV',                                   'Witch Rebirth: Strike the Vampire',                                                'translated'),  
		('Bodyguard of the Goddess',                             'Bodyguard of the Goddess',                                                         'translated'),  
		('Heavenly Divine Doctor',                               'Heavenly Divine Doctor',                                                           'translated'),  
		('Our Binding Love',                                     'Our Binding Love: My Gentle Tyrant',                                               'translated'),  
		('Maouyome',                                             'Maouyome',                                                                         'translated'),  
		('PRC',       'PRC',                      'translated'),  
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	urlfrag = [
		('wordexcerpt.com/series/guide-to-raising-a-supporting-male-lead/',           'Guide to Raising a Supporting Male Lead',       'translated'),
		('wordexcerpt.com/series/ankoku-kishi-monogatari/',                           'Ankoku Kishi Monogatari',                       'translated'),
		('wordexcerpt.com/series/real-cheat-online/',                                 'Real Cheat Online',                             'translated'),
		('wordexcerpt.com/series/wn-seirei-gensouki/',                                'Seirei Gensouki (WN)',                          'translated'),
		('wordexcerpt.com/series/quick-transmigration/',                              'Quick Transmigration: Fate Trading System',     'translated'),
		('wordexcerpt.com/series/behemoths-pet/',                                     'Behemoth\'s Pet',                               'translated'),  
		('wordexcerpt.com/series/golden-age-of-phoenix/',                             'Golden Age of Phoenix',                         'translated'),
		('wordexcerpt.com/series/rebirth-of-the-tyrants-pet/',                        'Rebirth of the Tyrant\'s Pet',                  'translated'),
		('wordexcerpt.com/series/desire/',                                            'Desire',                                        'translated'),  
		('wordexcerpt.com/series/irsc/',                                              'I Refuse to be a Supporting Character',         'translated'),  


		# ('https://wordexcerpt.com/series/15248527/',                                                 'Dracula', 'oel'),
		# ('https://wordexcerpt.com/series/87252129/',                                                 'The Call of Cthulhu', 'oel'),
		('wordexcerpt.com/series/75370994/',                                                 'Map to Hope',                                                 'oel'),
		('wordexcerpt.com/series/apollos-heart/',                                            'Apollo\'s Heart',                                             'oel'),
		('wordexcerpt.com/series/beatrice/',                                                 'Beatrice',                                                    'oel'),
		('wordexcerpt.com/series/disciple-of-immortal/',                                     'Disciple of Immortal',                                        'translated'),
		('wordexcerpt.com/series/former-general-is-undead-knight/act-1-resurrected-knight/', 'Former General Is Undead Knight',                             'translated'),
		('wordexcerpt.com/series/heavenly-divine-doctor-abandoned-concubine/',               'Heavenly Divine Doctor: Abandoned Concubine',                 'translated'),
		('wordexcerpt.com/series/his-transmigrated-cannon-fodder-fiance/',                   'His Transmigrated Cannon Fodder Fiancé',                      'translated'),
		('wordexcerpt.com/series/i-dont-want-to-be-loved/',                                  'I Don’t Want to Be Loved',                                    'translated'),
		('wordexcerpt.com/series/i-pulled-the-sword-and-became-the-heroine/',                'I Pulled the Sword and Became the Heroine?!',                 'translated'),
		('wordexcerpt.com/series/i-raised-a-black-dragon/',                                  'I Raised A Black Dragon',                                     'translated'),
		('wordexcerpt.com/series/i-should-have-read-the-ending/',                            'I Should Have Read The Ending',                               'translated'),
		('wordexcerpt.com/series/jujutsushi-wa-yuusha-ni-narenai/',                          'Jujutsushi Wa Yuusha Ni Narenai',                             'translated'),
		('wordexcerpt.com/series/lady-to-queen/',                                            'Lady To Queen',                                               'translated'),
		('wordexcerpt.com/series/living-as-the-villainess-queen/',                           'Living As the Villainess Queen',                              'translated'),
		('wordexcerpt.com/series/pet-addiction-the-princes-desire-to-spoil-his-pet/',        'Pet Addiction: The Prince’s Desire to Spoil His Pet',         'translated'),
		('wordexcerpt.com/series/predatory-marriage/',                                       'Predatory Marriage',                                          'oel'),
		('wordexcerpt.com/series/rebirth-entertainment-my-cold-gentle-husband/',             'Rebirth Entertainment: My Cold Gentle Husband',               'translated'),
		('wordexcerpt.com/series/remarried-empress/',                                        'Remarried Empress',                                           'translated'),
		('wordexcerpt.com/series/return-of-the-female-knight/',                              'Return of the Female Knight',                                 'translated'),
		('wordexcerpt.com/series/s-rank-behemoth-monster/',                                  'I’m An S-Rank Behemoth Monster',                              'translated'),
		('wordexcerpt.com/series/seirei-gensouki/',                                          'Seirei Gensouki: Spirit Chronicles (WN)',                     'translated'),
		('wordexcerpt.com/series/sword-of-gluttony-queen/act-1-magic-sword-of-gluttony/',    'Sword of Gluttony',                                           'translated'),
		('wordexcerpt.com/series/the-dukes-imposter-sister/',                                'The Duke’s Imposter Sister',                                  'translated'),
		('wordexcerpt.com/series/the-editor-is-the-novels-extra/',                           'The Editor Is the Novel’s Extra',                             'translated'),
		('wordexcerpt.com/series/the-former-wife-of-invisible-wealthy-man/',                 'The Former Wife of Invisible Wealthy Man',                    'translated'),
		('wordexcerpt.com/series/transmigration-raising-the-child-of-the-male-lead-boss/',   'Transmigration: Raising the Child of the Male Lead Boss',     'translated'),
		('wordexcerpt.com/series/under-the-oak-tree/',                                       'Under the Oak Tree',                                          'translated'),
		('wordexcerpt.com/series/villainess-and-the-stalker/',                               'Villainess and the Stalker',                                  'translated'),

		('rebirth.online/novel/earths-core' ,          "Earth's Core", 'oel'),
	]

	for key, name, tl_type in urlfrag:
		if key in item['linkUrl'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False