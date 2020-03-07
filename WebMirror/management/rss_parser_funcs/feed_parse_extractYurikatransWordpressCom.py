def extractYurikatransWordpressCom(item):
	'''
	Parser for 'yurikatrans.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	titlemap = [
		('Arms Otome Ch',             'Arms Otome',                                                                             'translated'),
		('Levelmaker',                'Levelmaker -Raising Levels While Living in Another World-',                              'translated'),
		('The Strongest Fairy',       'Is the strongest in another world a hero? a demon lord? No! it’s a fairy desu!',         'translated'),
		('Eiyuu no Musume Chapter ',  'Eiyuu no Musume to Shite Umarekawatta Eiyuu wa Futatabi Eiyuu o Mezasu (WN) ',           'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	tagmap = [
		('The Pebble',                                   'I am just a〈Former〉Pebble! ~The Healing Golem and Monster User~',                                             'translated'),
		('The Strongest Fairy',                          'Is the strongest in another world a hero? a demon lord? No! it’s a fairy desu!',                                'translated'),
		('Levelmaker',                                   'Levelmaker -Raising Levels While Living in Another World-',                                                     'translated'),
		('I Reincarnated',                               'I Was Reincarnated but I Don\'t Know Why',                                                                      'translated'),
		('Vampire Yukine',                               'Vampire Yukine\'s Otherworld Journey',                                                                          'translated'),
		('Fief Strengthening',                           'Fief Strengthening',                                                                                            'translated'),
		('Vampire Princess',                             'Vampire Princess',                                                                                              'translated'),
		('Arms Otome',                                   'Arms Otome',                                                                                                    'translated'),
		('Eiyuu Musume',                                 'Eiyuu no Musume to Shite Umarekawatta Eiyuu wa Futatabi Eiyuu o Mezasu (WN)',                                   'translated'),
		('eiyuu no musume',                              'Eiyuu no Musume to Shite Umarekawatta Eiyuu wa Futatabi Eiyuu o Mezasu (WN)',                                   'translated'),
		('Goddess',                                      'Being Recognized as an Evil God, I Changed My Job to Guardian Deity of the Beastmen Country',                   'translated'),
		('dungeon master',                               'I Became a 《Dungeon Master》 In a Different World',                                                            'translated'),
		('Daybreak Summoner',                            'Daybreak Summoner ～I will protect that girl who summoned me into this world with everything I’ve got～!',      'translated'),
		('Luggage Carrier Dragon Slayer',                'Luggage Carrier Dragon Slayer!',                                                                                'translated'),
		('Kansutoppu',                                   'Kansutoppu!',                                                                                                   'translated'),
		('saint mari',                                   'Emblem of the Incarnated Saint and the Dragon ～The Airheaded Goddess aims to be a top Adventurer～',           'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	return False