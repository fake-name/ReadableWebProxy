def extractRainbowTurtleTranslations(item):
	"""
	Rainbow Turtle Translations
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'LMS' in item['tags']:
		return buildReleaseMessageWithType(item, 'Legendary Moonlight Sculptor', vol, chp, frag=frag, postfix=postfix)
	if 'dungeon hunter' in item['tags']:
		return buildReleaseMessageWithType(item, 'Dungeon Hunter', vol, chp, frag=frag, postfix=postfix)
	if 'DKG' in item['tags']:
		return buildReleaseMessageWithType(item, "The Demon King's Game", vol, chp, frag=frag, postfix=postfix)
		
	tagmap = [
		('Omniscient Reader\'s Viewpoint',             'Omniscient Reader\'s Viewpoint',                         'translated'),
		('Game Loading',                               'Game Loading',                                           'translated'),
		('Earth is Online',                            'Earth is Online',                                        'translated'),
		('Game Live Broadcast',                        'Game Live Broadcast',                                    'translated'),
		('Rebirth of a Supermodel',                    'Rebirth of a Supermodel',                                'translated'),
		('card room',                                  'card room',                                              'translated'),
		('cr',                                         'card room',                                              'translated'),
		('God Level Summoner',                         'God Level Summoner',                                     'translated'),
		('GLS',                                        'God Level Summoner',                                     'translated'),
		('DS',                                         'Dimensional Sovereign',                                  'translated'),
		('STB',                                        'I\'m Not Shouldering this Blame',                        'translated'),
		('Dangerous Survival in the Apocalypse',       'Dangerous Survival in the Apocalypse',                   'translated'),
		('DSA',                                        'Dangerous Survival in the Apocalypse',                   'translated'),
		('i\'m not human',                             'I\'m not human',                                         'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
	return False