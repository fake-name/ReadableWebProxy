def extractPathOfTranslation(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if item['title'].startswith('Path of Discord Episode'):
		return None


	snames = [
			"Emperor's Domination",
			'Martial God Realm',
			'Big Life',
			"I'm a Villain",
			'Grasping Evil',
			'The Human Emperor',
			"Post-80's Cultivation Journal",
		]

	tlut = {tmp.lower(): tmp for tmp in snames}


	ltags = [tmp.lower() for tmp in item['tags']]
	for key, value in tlut.items():
		if key in ltags:
			return buildReleaseMessageWithType(item, value, vol, chp, frag=frag, postfix=postfix)

	chp_prefixes = [
			('He\'s the Legendary Guard, Isn\'t He?',                True), 
			('Black Iron\'s Glory',                                  True), 
			('Spiritual furnace',                                    True), 
			('Possessing Nothing',                                   True), 
			('Lord of the Star Ocean',                               True), 
			('The Ancestor of our Sect Isn’t Acting like an Elder',  True), 
			('Dragon-Marked War God',                                False), 
			('The Daoist Seal',                                      True), 
			('Eternal Life',                                         True), 
			('When God Made Me',                                     True), 
			('Big Life',                                             True), 
			('Deva Wizard',                                          True), 
			('Urban Banished Immortal',                              True), 
			('The Prodigy Daughter Of The Medicine God',             True), 
			('Emperor of Tomorrow',                                  True), 
			('ID – The Greatest Fusion Fantasy',                     True), 
			('God Hunter',                                           True), 
			('Immortal',                                             True), 
			('Martial Emperor Reborn ',                              True), 
			('Martial God Conqueror',                                True),
			('My Wife Is a Beautiful CEO',                           True),
			('World Defying Dan God',                                True), 
			('Game Market 1983',                                     False), 
			('Spirit Vessel',                                        False), 
			('Instant Kill',                                         False), 
			('My Daoist Life',                                       False), 
			('Tales of the Reincarnated Lord',                       False), 
			('Cohen of the Rebellion',                               False), 
			('Post-’80s Cultivation Journal',                        False), 
			('Immortal',                                             False), 
			('Everlasting Immortal Firmament -',                     False),
			('The Great Game',                                       False), 
			('Grasping Evil',                                        False), 
			('My Cold and Beautiful Wife',                           False), 
			('The Daoist Seal',                                      False), 
		]

	for series, require_chp in chp_prefixes:
		if item['title'].lower().startswith(series.lower()) and (not require_chp or 'chapter' in item['title'].lower()):
			return buildReleaseMessageWithType(item, series, vol, chp, frag=frag, postfix=postfix)
			
	return False