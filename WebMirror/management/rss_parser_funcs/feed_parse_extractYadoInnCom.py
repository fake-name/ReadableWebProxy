def extractYadoInnCom(item):
	'''
	Parser for 'yado-inn.com'
	'''

	if 'Manga' in item['tags']:
		return None

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('SHS',                               'Super High Schoolers Affording to Live in Another World',                                     'translated'),
		('MLW',                               'While killing slimes for 300 years, I became the MAX level unknowingly',                      'translated'),
		('remake',                            'Remake Our Life!',                                                                            'translated'),
		('aristocrat assassin',               'aristocrat assassin',                                                                         'translated'),
		('reincarnated maid',                 'Reincarnated Maid is About To Be Captured by All Players',                                    'translated'),
		('gorgeous beauty',                   'Transformed into a Gorgeous Beauty',                                                          'translated'),
		('JUSCO',                             'JUSCO',                                                                                       'translated'),
		('TGWSPUJ',                           'The Girl Who Spits Up Jewels',                                                                'translated'),
		('ABM',                               'Akugyaku no Black Maria',                                                                     'translated'),
		('IDK',                               'Only I Who Got The Initial Job As Demon King',                                                'translated'),
		('MG',                                'Magi’s Grandson',                                                                             'translated'),
		('DD',                                'Common Sense of a Duke\'s Daughter',                                                          'translated'),
		('Komachi',                           'Chronicles of The Hardships of Komachi in The Sengoku Era',                                   'translated'),
		('Wiseman',                           'She Professed Herself The Pupil Of The Wiseman (WN)',                                         'translated'),
		('Little Sage',                       'The Small Sage Will Try Her Best In The Different World From Lv.1!',                          'translated'),
		('Noble Reincarnation',               'Noble Reincarnation~Blessed With the Strongest Power From Birth',                             'translated'),
		('rebirth',                           'Rebirth of the Heavenly Demon',                                                               'translated'),
		('murabito',                          'Murabito Desuga Nanika',                                                                      'translated'),
		('Dahlia',                            'Magical Devices Craftsman Dahlia Won’t Hang Her Head Down Anymore',                           'translated'),
		('Goc',                               'God of Cooking',                                                                              'translated'),
		('WSR',                               'World Strongest Rearguard',                                                                   'translated'),
		('Imouto',                            'Reincarnated as My Little Sister',                                                            'translated'),
		('villainess’ father',                'Since I’ve Reincarnated as the Villainess’ Father, I’ll Shower My Wife and Daughter in Love', 'translated'),
		('loli witch',                        'I Became a Magical Cheat Loli Witch ~My Different World Life With My Reincarnation Privilege [Creation Magic] and the [Seed of Magic]~', 'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	titlemap = [
		('MLW – Chapter ',                     'While killing slimes for 300 years, I became the MAX level unknowingly',      'translated'),
		('SKM – Chapter ',                     'Chronicles of The Hardships of Komachi in The Sengoku Era',                   'translated'),
		('OP Waifus Chapter ',                 'Being Able to Edit Skills in Another World, I Gained OP Waifus',              'translated'),
		('ABM – Chapter ',                     'Akugyaku no Black Maria',                                                     'translated'),
		('Magi’s Grandson – ',                 'Magi’s Grandson',                                                             'translated'),
		('Pervy Healer ',                      'I Work As A Healer In Another World’s Labyrinth City',                        'translated'),
		('MLW ',                               'While killing slimes for 300 years, I became the MAX level unknowingly',      'translated'),
		('Cheat na Kaineko – Chapter ',        'Cheat na Kaineko no Okage de Rakuraku Level Up',                              'translated'),
		('JUSCO',                              'JUSCO',                                                                       'translated'),
		('Magi’s Grandson Chapter ',           'Magi\'s Grandson',                                                            'translated'),
		('Dahlia – Chapter ',                  'Magical Devices Craftsman Dahlia Won’t Hang Her Head Down Anymore',           'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False