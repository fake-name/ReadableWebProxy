def extractReLibrary(item):
	"""
	'Re:Library'
	"""
	if item['tags'] == ['rhapsody of mulan']:
		return None

	
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
		
	tagmap = [
		('Starting Anew as the New Me',            'Starting Anew as the New Me',                                            'translated'),
		('Mysterious World Beast God',             'Mysterious World Beast God',                                             'translated'),
		('Abyss Domination',                       'Abyss Domination',                                                       'translated'),
		('The Demon King\'s Daughter',             'The Demon King\'s Daughter',                                             'translated'),
		('Very Pure & Ambiguous - The Prequel',    'Very Pure & Ambiguous - The Prequel',                                    'translated'),
		('Barrier Master Reincarnation',           'Barrier Master Reincarnation',                                           'translated'),
		('6-Year Old Sage',                        '6-Year Old Sage',                                                        'translated'),
		('World of Immortals',                     'World of Immortals',                                                     'translated'),
		('Bu ni mi',                               'Bu ni Mi wo Sasagete Hyaku to Yonen. Elf de Yarinaosu Musha Shugyou',    'translated'),
		('Magic Language',                         'No matter how you look at it, this world\'s magic language is Japanese', 'translated'),
		('High Comprehension Low Strength',        'High Comprehension Low Strength',                                        'translated'),
		('Otherworld Nation Founding Chronicles',  'Otherworld Nation Founding Chronicles',                                  'translated'),
		('Arifureta',                              'Arifureta Shokugyou de Sekai Saikyou (WN)',                              'translated'),
		('Author Reincarnated',                    'The Author Reincarnated?!',                                              'translated'),
		('The Strongest System',                   'The Strongest System',                                                   'translated'),
		('Outcast Magician',                       'Outcast Magician and the Power of Heretics',                             'translated'),
		('Nine Yang Sword Saint',                  'Nine Yang Sword Saint',                                                  'translated'),
		('God of Chaos',                           'God of Chaos',                                                           'oel'),
		('Soft Spoken Brutality',                  'Soft Spoken Brutality',                                                  'oel'),
		('Martial Void King',                      'Martial Void King',                                                      'oel'),
		('Aurora God',                             'Aurora God',                                                             'oel'),
		("Silva's Diary",                          "Silva's Diary",                                                          'oel'),
		('Dragon Princess',                        'Even if I\'m Reborn as a Cute Dragon Girl, I will still make a Harem',   'translated'),
		('female knight & dark elf',               'The Life of a Female Knight and a Dark Elf',                             'translated'),
		('Shield Hero',                            'Tate no Yuusha no Nariagari',                                            'translated'),
		('succubus in another world',              'Succubus-san\'s Life in a Another World',                                'translated'),
		('not sure, another world reincarnation',  'Not Sure, But It Looks Like I Got Reincarnated in Another World',        'translated'),
		('the ancestor of our sect',               'The Ancestor of our Sect Isn’t Acting like an Elder',                    'translated'),
		('hero\'s daughter',                       'Reborn as the Hero\'s Daughter! Time to Become the Hero Once More!',     'translated'),
		('reborn as a transcendence',              'reborn as a transcendent',                                               'translated'),
		('reborn as a transcendent',               'reborn as a transcendent',                                               'translated'),
		('life with a tail',                       'life with a tail',                                                       'translated'),
		('pupil of the wiseman',                   'She Professed Herself The Pupil Of The Wiseman',                         'translated'),
		('Levelmaker',                             'Levelmaker',                                                             'translated'),
		('Demon Sword Maiden',                     'Demon Sword Maiden',                                                     'translated'),
		('the saintess',                           'How can the Saintess be a Boy!?',                                                                                                 'translated'),
		('disappointing princesses',               'Two as One Disappointing Princesses Want to Live Free ',                                                                          'translated'),
		('Vampire Princess',                       'I Became a Vampire Princess after Reincarnation!? Building The Strongest Yuri Harem Using the Cheat Skill 【Demon Lord】!',       'translated'),
		('Stained Red',                            'Stained Red',                                                                                                                     'oel'),
		('Truth & Myth - The Awakening',           'Truth & Myth - The Awakening',                                                                                                    'oel'),
		
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	return False