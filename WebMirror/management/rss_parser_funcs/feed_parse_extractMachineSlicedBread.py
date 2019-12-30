def extractMachineSlicedBread(item):
	"""

	"""
	
	if item['title'].startswith("Protected: "):
		return None
	if item['title'].startswith("NTR Crush "):
		return None
	if item['title'].startswith("World of Women "):
		return None
	if item['title'].startswith("Enslaved Sister Harem"):
		return None
	if "(Locked)" in item['title']:
		return None
	
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
		
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	tagmap = [
		('Inma no Hado TL',                             'Inma no Hado',                                                                                                                  'translated'),
		('Charm TL',                                    'I made a slave harem using a charm cheat in a different world.',                                                                'translated'),
		('Loli Manko TL',                               'Kyonkon na Ore ga Rori ma●ko Bishoujo wo Okashite Kopitte, Ohime-sama wo Torimodosu Isekai Tan',                                'translated'),
		('Cheatman TL',                                 'Joudan Mitaina Chiito Nouryouku de Isekai ni Tensei shi, Sukikatte suru Hanashi',                                               'translated'),
		('Zombie Emperor TL',                           'The Bloodshot One-Eyed Zombie Emperor',                                                                                         'translated'),
		('Asuka TL',                                    'Asuka of the Scarlet Sky ~ The Female Hero who Degraded to a Licentious and Wicked Person~',                                    'translated'),
		('Flight, Invisibility, and Teleportation TL',  'If You Got the Power of Flight, Invisibility, and Teleportation, What Would You Do?',                                           'translated'),
		('Class TL',                                    'Dragged into the class transfer ~For some reason I was dragged into the transfer with the girl class so I will make a harem!~', 'translated'),
		('Kininaru TL',                                 'Kininaru Kanojo wo Tokoton Okashi Tsukusu Hanashi',                                                                             'translated'),
		('Grassland TL',                                'Sougen no Okite ~Shii yatsu ga moteru, ii buzoku ni umarekawatta zo~',                                                          'translated'),
		('Kemono TL',                                   'Flirting with beast girls! Doing nothing but copulation!',                                                                      'translated'),
		('Game World TL',                               'After Reincarnating Into This Game World I Seemed to Have Taken Over the Control of Status',                                    'translated'),
		('Hero TL',                                     'Hero Manufacturing Machine ~A Job to Make Children~',                                                                           'translated'),
		('Inmajutsu TL',                                'Ore ga Inmajutsu de Dorei Harem wo Tsukuru Hanashi',                                                                            'translated'),
		('Yandere TL',                                  'My elder sister fell in love with me and transformed into a yandere',                                                           'translated'),
		('Semen TL',                                    'Curing Incurable Disease With Semen',                                                                                           'translated'),
		('Step-sisters(?) TL',                          'The life I started with my step-sisters(?)',                                                                                    'translated'),
		('Ero Gacha',                                   'Ero Gacha',                                                                                                                     'translated'),
		('Xray TL',                                     'X-ray Is More Than I Thought',                                                                                                  'translated'),
		('Betrayed Hero TL',                            'Summoned as a Hero, but I got betrayed.',                                                                                       'translated'),
		('Netori TL',                                   'Because I was excluded out of the class transfer, I decided to steal my classmate’s lover',                                     'translated'),
		('Pure Love x Insult Complex',                  'Pure Love x Insult Complex',                                                                                                    'translated'),
		('Beauty Reversal TL',                          'In a World Where Beauty is Reversed, a Harem Only for Me.',                                                                     'translated'),
		
		
		('Elf TL',                             'Elf no Kuni no Kyuutei Madoushi ni Naretanode, Toriaezu Himesama ni Seitekina Itazura wo Shitemimashita',                                'translated'),
		('Erocom TL',                          'I’m sorry for getting a head start but I decided to live everyday erotically',                                                           'translated'),
		('Taneuma',                            'Isekai Taneuma',                                                                                                                         'translated'),
		('Time and Place',                     'The Timefall Saga : Time and Place',                                                                                                     'oel'),
		('The Lust System',                    'The Lust System',                                                                                                                        'oel'),
		('Sins of Love',                       'Sins of Love',                                                                                                                           'oel'),
		('world of martial porn',              'World of Martial Porn',                                                                                                                  'oel'),
		('World of Women',                     'World of Women',                                                                                                                         'oel'),
		('Power of Creation',                  'Power of Creation',                                                                                                                      'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
	titlemap = [
		('Elf ',                                                                     'Elf no Kuni no Kyuutei Madoushi ni Naretanode, Toriaezu Himesama ni Seitekina Itazura wo Shitemimashita',                     'translated'),
		('Netori ',                                                                  'Because I was excluded out of the class transfer, I decided to steal my classmate’s lover',                                   'translated'),
		('Half elves fall in love chapter ',                                         'Half elves fall in love',                                                                                                     'translated'),
		('Gacha Chapter ',                                                           'Ero Gacha',                                                                                                                   'translated'),
		('Erocom Chapter ',                                                          'I\'m sorry for getting a head start but I decided to live everyday erotically',                                               'translated'),
		('PLIC Chapter ',                                                            'Pure Love x Insult Complex',                                                                                                  'translated'),
		('Inma no Hado ch.',                                                         'Inma no Hado',                                                                                                                'translated'),
		('Inma no Hado chapter',                                                     'Inma no Hado',                                                                                                                'translated'),
		('Hero Pandemic chapter',                                                    'I became a Hero in Pandemic',                                                                                                 'translated'),
		('X-ray is more than I thought Chapter ',                                    'X-ray Is More Than I Thought',                                                                                                'translated'),
		('Tales of a Seductress – Chapter',                                          'Tales of a Seductress',                                                                                                       'oel'),
		('Tales of Seductress – Chapter',                                            'Tales of a Seductress',                                                                                                       'oel'),
		('The Power of Creation – Chapter',                                          'The Power of Creation',                                                                                                       'oel'),
		('The Power of Creation Chapter',                                            'The Power of Creation',                                                                                                       'oel'),
		('Dragon Magic Chapter ',                                                    'Dragon Magic',                                                                                                                'oel'),
		('Just a Guy in Space – ',                                                   'Just a Guy in Space',                                                                                                         'oel'),
		('Just a Guy in Space – ',                                                   'Just a Guy in Space',                                                                                                         'oel'),
		('Tales of an Enchantress – Chapter',                                        'Tales of an Enchantress',                                                                                                     'oel'),
		('Min’s Story – Chapter ',                                                   'Min’s Story',                                                                                                                 'oel'),
		('ISSL Chapter',                                                             'International Sex Slave Law',                                                                                                 'oel'),
		('Lute Dragoon – Chapter ',                                                  'Lute Dragoon',                                                                                                                'oel'),
		('NTR System – Chapter ',                                                    'NTR System',                                                                                                                  'oel'),
		('Cheat Parody Chapter ',                                                    'Cheat Parody',                                                                                                                'oel'),
		('The Sex Beast System Chapter ',                                            'The Sex Beast System',                                                                                                        'oel'),
		('TLGPL Chapter ',                                                           'The Ladies Gang Puppet Leader',                                                                                               'oel'),
		('FeralHeart ',                                                              'FeralHeart',                                                                                                                  'oel'),
		('Kama-sutra Chapter ',                                                      'Kama-sutra',                                                                                                                  'oel'),
		('Evil Prophet Chapter ',                                                    'The Evil Prophet',                                                                                                            'oel'),
		('STC Chapter ',                                                             'Swayamvar: Tamer Chronicles',                                                                                                 'oel'),
		('The World of Women – Chapter ',                                            'The World of Women',                                                                                                          'oel'),
		('Bonded Goddess – Chapter ',                                                'I Went To Another World and Bonded With a Goddess So I Might As Well Have Lots of Sex and Rub it In My Ex-wife’s Face',       'oel'),
		('I Will Cuck Every God and Fuck Every Goddess For My Revenge! Chapter ',    'I Will Cuck Every God and Fuck Every Goddess For My Revenge!',                                                                'oel'),
		('The Lust System',                    'The Lust System',                                                                                                                        'oel'),
		
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
	return False