def extractLetsyuriWordpressCom(item):
	'''
	Parser for 'letsyuri.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('icgsf',             'I, Cute Grass, am Super Fierce!',                 'translated'),
		('ftbtceo',           'Forced to Become The CEO',                        'translated'),
		('summon survival',   'Summon Survival',                                   'translated'),
		('gtvf',              'Green Tea Villainess Fails',                        'translated'),
		('ecfshm',            'Former Cannon Fodder’s Self-Help Manual',           'translated'),
		('sodi',              'Stranded on a Deserted Island, What to Do?',        'translated'),
		('vwccs',             'Villainess With Cat Changing System',               'translated'),
		('Asura',             'Transmigrated Into a Smashing Asura Girl',                      'translated'),
		('movie queen',       'Being Raised as a Baby by the Movie Queen',                      'translated'),
		('vipu',              'Villainess, I’ll Pamper You',                      'translated'),
		('vipy',              'Villainess, I’ll Pamper You',                      'translated'),
		('abmb',              'After Being Marked, I Have a Baby',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	titlemap = [
		('BRMQ ',                                        'Being Raised as a Baby by the Movie Queen',          'translated'),
		('TISAG ',                                        'Transmigrated Into a Smashing Asura Girl',          'translated'),
		('Summon Survival',                               'Summon Survival',                                   'translated'),
		('Green Tea Villainess Fails',                    'Green Tea Villainess Fails',                        'translated'),
		('Former Cannon Fodder’s Self-Help Manual',       'Former Cannon Fodder’s Self-Help Manual',           'translated'),
		('Stranded on a Deserted Island, What to Do?',    'Stranded on a Deserted Island, What to Do?',        'translated'),
		('I, Cute Grass, am Super Fierce! Chapter ',      'I, Cute Grass, am Super Fierce!',                   'translated'),
		('Forced to Become The CEO Chapter ',             'Forced to Become The CEO',                          'translated'),
		('Villainess With Cat Changing System Chapter ',  'Villainess With Cat Changing System',               'translated'),
		('XCF ',                                          'Former Cannon Fodder’s Self-Help Manual',           'translated'),
		('Tensei Shoujo no Rirekisho',  'Tensei Shoujo no Rirekisho',      'translated'),
		('Master of Dungeon',           'Master of Dungeon',               'oel'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



	return False