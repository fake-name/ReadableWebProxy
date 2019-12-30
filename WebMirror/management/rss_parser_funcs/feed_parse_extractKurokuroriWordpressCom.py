def extractKurokuroriWordpressCom(item):
	'''
	Parser for 'kurokurori.wordpress.com'
	'''

	
	badwords = [
			'loli wife',     # Manga
			'I\'m Strong',   # Manga
		]
	if any([bad in item['tags'] for bad in badwords]):
		return None



	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Villainess with Weapons',       'The Villainess Will Crush Her Destruction End Through Modern Firepower',                                                'translated'),
		('Saving 80000 Gold',             'Saving 80,000 Gold in Another World for Retirement ',                                                                   'translated'),
		('Saving 80,000 Gold',            'Saving 80,000 Gold in Another World for Retirement ',                                                                   'translated'),
		('Survive Using Potion',          'Potion-danomi de Ikinobimasu!',                                                                                         'translated'),
		('Former Assassin',               'Killing with Bikini Armor ~Former assassin sees a dream of huge breasts over the steam boundary~',                      'translated'),
		('Demon King',                    'Do you think someone like you can defeat the demon king?',                                                              'translated'),
		('Fathercon Daughters',           'The Middle-aged Man who just Returned from Another World Melts his Fathercon Daughters with his Paternal Skill ',       'translated'),
		('Genocide Online',               'Genocide Online ~Playtime Diary of an Evil Young Girl~',                                                                'translated'),
		('Disciple Yandere',              'I Was Made The Disciple of a Yandere, but…',                                                                            'translated'),
		('lolita vampire',                'The Strongest Vampire Princess Wants a Little Sister!!',                                                                'translated'),
		('slime 300 years',               'While Killing Slimes for 300 Years, I Became the MAX Level Unknowingly',                                                'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False