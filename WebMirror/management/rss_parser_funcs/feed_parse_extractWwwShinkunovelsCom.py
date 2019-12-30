def extractWwwShinkunovelsCom(item):
	'''
	Parser for 'www.shinkunovels.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tag_title_map = [
		('Hidden Dungeon',                                'The Hidden Dungeon Only I Can Enter',                                              'translated'),
		('Black Summoner',                                'Black Summoner',                                                                   'translated'),
		('Levelmaker',                                    'Levelmaker',                                                                       'translated'),
		('Arms Otome',                                    'Arms Otome',                                                                       'translated'),
		('Inumimi Dorei',                                 'Inumimi Dorei',                                                                    'translated'),
		('Underground Dungeon',                           'Underground Dungeon',                                                              'translated'),
		('Former hero adventurer',                        'Former Hero Adventurer, Disciple Slave Girl',                                      'translated'),
		('No Fatigue',                                    'No Fatigue',                                                                       'translated'),
		('Seijo no Kaifuku',                              'Seijo no Kaifuku Mahou ga Dou Mitemo Ore no Rekkaban na Ken ni Tsuite',            'translated'),
		('Middle Aged Adventurer Kein’s good deed',       'Middle Aged Adventurer Kein’s good deed',                                          'oel'),
		('Middle Aged Adventurer Kein\'s good deed',      'Middle Aged Adventurer Kein’s good deed',                                          'oel'),
		('Curse Sword Master',                            'Cursed Sword Master',                                                              'translated'),
		('Curse Sword Master Chapter ',                   'Cursed Sword Master',                                                              'translated'),
		('No Fatigue Chapter',                            'No Fatigue',                                                                       'translated'),
		('Seijo no Kaifuku Chapter',                      'Seijo no Kaifuku Mahou ga Dou Mitemo Ore no Rekkaban na Ken ni Tsuite',            'translated'),
		('Seijo no Kaifuku Release',                      'Seijo no Kaifuku Mahou ga Dou Mitemo Ore no Rekkaban na Ken ni Tsuite',            'translated'),
		('The Strongest Fairy Adventurer',                'Is the strongest in another world a hero? a demon lord? No! it’s a fairy desu!',   'translated'),
	]

	for tagname, name, tl_type in tag_title_map:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	if 'Seijo no Kaifuku Chapter ' in item['title']:
		return buildReleaseMessageWithType(item, 'Seijo no Kaifuku Mahou ga Dou Mitemo Ore no Rekkaban na Ken ni Tsuite', vol, chp, frag=frag, postfix=postfix, tl_type='translated')


	for titlecomponent, name, tl_type in tag_title_map:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False