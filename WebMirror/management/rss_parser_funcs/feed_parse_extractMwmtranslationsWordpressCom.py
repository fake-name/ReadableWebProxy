def extractMwmtranslationsWordpressCom(item):
	'''
	Parser for 'mwmtranslations.wordpress.com'
	'''


	badwords = [
			'dawn of the witch',    # Manga
		]
	if any([bad in item['tags'] for bad in badwords]):
		return None



	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('The Villainess Blooms',                                                                                                                         'The Villainess Blooms',                                                                                                                                        'translated'),
		('Even Though I\'m a Former Noble and a Single Mother, My Daughters are too Cute and Working as an Adventurer Isn\'t Too Much of a Hassle',       'Even Though I\'m a Former Noble and a Single Mother, My Daughters are too Cute and Working as an Adventurer Isn\'t Too Much of a Hassle',                      'translated'),
		('Old Vampire and a Holy Girl',                                                                                                                   'Old Vampire and a Holy Girl',                                                                                                                                  'translated'),
		('Akuyaku Reijou wa Danna-sama wo Yasesasetai',                                                                                                   'Akuyaku Reijou wa Danna-sama wo Yasesasetai',                                                                                                                  'translated'),
		('Senpensekai no Madoushi',                                                                                                                       'Senpensekai no Madoushi',                                                                                                                                      'translated'),
		('Did You Know That a Playboy Can Change His Job to a Sage?',                                                                                     'Did You Know That a Playboy Can Change His Job to a Sage?',                                                                                                    'translated'),
		('Playboy',                                                                                                                                       'Did You Know That a Playboy Can Change His Job to a Sage?',                                                                                                    'translated'),
		('The Splendid Daily Life of the Mother Devouring Princess',                                                                                      'The Splendid Daily Life of the Mother Devouring Princess',                                                                                                     'translated'),
		('Endo and Kobayashi\'s Live Commentary on the Villainess',                                                                                       'Endo and Kobayashi\'s Live Commentary on the Villainess',                                                                                                      'translated'),
		('Since I’ve Reincarnated as the Villainess’ Father, I’ll Shower My Wife and Daughter in Love',       'Since I’ve Reincarnated as the Villainess\' Father, I\'ll Shower My Wife and Daughter in Love',                      'translated'),
		('The Earl\'s Daughter was Suddenly Employed as the Crown Prince\'s Fiancée',                         'The Earl\'s Daughter was Suddenly Employed as the Crown Prince\'s Fiancée',                                          'translated'),
		('auto assigned villainess',                                                                          'auto assigned villainess',                                                                                           'translated'),
		('magical revolution',                                                                                'The Magical Revolution of the Reincarnated Princess and the Genius Young Lady',                                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	titlemap = [
		('The Villainess Blooms',                                                                       'The Villainess Blooms',                                                          'translated'),
		('The Villainess Will Crush Her Destruction End Through Modern Firepower – ',                   'The Villainess Will Crush Her Destruction End Through Modern Firepower',         'translated'),
		('Kochugunshikan Boukensha ni Naru',                                                            'Kochugunshikan Boukensha ni Naru',                                               'translated'),
		('Tensei Shoujo no Rirekisho',  'Tensei Shoujo no Rirekisho',      'translated'),
		('Master of Dungeon',           'Master of Dungeon',               'oel'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False