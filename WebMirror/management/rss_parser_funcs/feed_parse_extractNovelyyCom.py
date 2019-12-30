def extractNovelyyCom(item):
	'''
	Parser for 'novelyy.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	# I think this is a TL pirate site?

	tagmap = [
		('Bringing the Nation&#039;s Husband Home',                                       'Bringing the Nation&#039;s Husband Home',                                         'translated'),
		('Infinite Competitive Dungeon Society',                                          'Infinite Competitive Dungeon Society',                                            'translated'),
		('Hachinan tte, Sore wa Nai Deshou!',                                             'Hachinan tte, Sore wa Nai Deshou!',                                               'translated'),
		('I’m Back in the Other World?',                                                  'I’m Back in the Other World?',                                                    'translated'),
		('Destroyer of Ice and Fire',                                                     'Destroyer of Ice and Fire',                                                       'translated'),
		('Martial God Conqueror',                                                         'Martial God Conqueror',                                                           'translated'),
		('Galactic Dark Net',                                                             'Galactic Dark Net',                                                               'translated'),
		('Legend of Ling Tian',                                                           'Legend of Ling Tian',                                                             'translated'),
		('Age of Cosmic Exploration',                                                     'Age of Cosmic Exploration',                                                       'translated'),
		('A Thought Through Eternity',                                                    'A Thought Through Eternity',                                                      'translated'),
		('The Magus Era',                                                                 'The Magus Era',                                                                   'translated'),
		('When A Mage Revolts',                                                           'When A Mage Revolts',                                                             'translated'),
		('23:11',                                                                         '23:11',                                                                           'translated'),
		('Omni-Magician',                                                                 'Omni-Magician',                                                                   'translated'),
		('Reincarnation Of The Strongest Sword God',                                      'Reincarnation Of The Strongest Sword God',                                        'translated'),
		('Although I am only level 1, but with this unique skill, I am the strongest',    'Although I am only level 1, but with this unique skill, I am the strongest',      'translated'),
		('Seijo no Kaifuku Mahou ga Dou Mitemo Ore no Rekkaban na Ken ni Tsuite',         'Seijo no Kaifuku Mahou ga Dou Mitemo Ore no Rekkaban na Ken ni Tsuite',           'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return None
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return None