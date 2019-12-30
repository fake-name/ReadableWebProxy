def extractMountainofPigeonsTranslations(item):
	"""
	Mountain of Pigeons Translations
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	
	if 'Manga' in item['tags']:
		return None
	if 'Anime' in item['tags']:
		return None

	tagmap = [
		('bahamut',                                    'Undefeated Bahamut Chronicle',                                                          'translated'),
		('HSN',                                        'Hataraku Maou-sama!',                                                                   'translated'),
		('Trinity Seven',                              'Trinity Seven',                                                                         'translated'),
		('log horizon',                                'Log Horizon',                                                                           'translated'),
		('GaWoRaRe',                                   'Kanojo ga Flag wo Oraretara',                                                           'translated'),
		('Rokujouma',                                  'Rokujouma no Shinryakusha!?',                                                           'translated'),
		('World Break',                                'Seiken Tsukai no World Break',                                                          'translated'),
		('Four Cours After',                           'Four Cours After',                                                                      'translated'),
		('Upon the Wind and Melody of the Lute',       'Upon the Wind and Melody of the Lute',                                                  'translated'),
		('MonsterTamer',                               'Monster Tamer’s Fluffy Master-Apprentice Life',                                         'translated'),
		('Magia',                                      'Revenge Magia of the Magic Breaker',                                                    'translated'),
		('Low-Life',                                   'Seishun Buta Yarou',                                                                    'translated'),
		('Hundred',                                    'Hundred',                                                                               'translated'),
		('ElfWife',                                    'I, a Demon Lord, Took a Slave Elf as my Wife, but how do I Love Her?',                  'translated'),
		('StarrySky',                                  'I Hold Your Voice Alone, Under The Starry Sky',                                         'translated'),
		('Maou-ppoi',                                  'Maou-ppoi no!',                                                                         'translated'),
		('KimiSen',                                    'Kimi to Boku no Saigo no Senjo, Aruiha Sekai ga Hajimaru Seisen',                       'translated'),
		('IseCafé',                                    'Have a Coffee After School, In Another World\'s Café',                                  'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	titlemap = [
		('Using My God Skill “Breathing” to Level Up, I Will Challenge the Dungeon of the Gods',  'Using My God Skill "Breathing" to Level Up, I Will Challenge the Dungeon of the Gods',      'translated'),
		('	The Strongest Mage’s Retirement Plan',                                                'Saikyou Mahoushi no Inton Keikaku',                                                         'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False