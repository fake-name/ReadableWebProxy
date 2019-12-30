def extractHonyaku(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	tagmap = [
		('pharmacist',  'Cheat Pharmacist’s Slow Life ~Making a Drug Store in Another World~',                                                                                                  'translated'),
		('kujonin',     'Kujonin',                                                                                                                                                              'translated'),
		('OVRMMO',      'Toaru Ossan no VRMMO Katsudouki (WN)',                                                                                                                                 'translated'),
		('VendM',       'Jidou Hanbaiki ni Umarekawatta ore wa Meikyuu o Samayou',                                                                                                              'translated'),
		('5th Son',     'The Cheeky Fifth Son of a Noble',                                                                                                                                      'oel'),
		('Cursed',      'Kousei Ishikawa is Cursed!',                                                                                                                                           'oel'),
		('Dragon',      'Dragon-chan Doesn’t Want to be Hunted',                                                                                                                                'oel'),
		('Wfb',         'Wizard with the flower blades',                                                                                                                                        'oel'),
		('OriginStory', 'OriginStory the VRMMO: The advent of AxeBear',                                                                                                                         'oel'),
		('Fluvia',      'Fluvia Dellarose was Supposed to be an Otome Game’s Mini-Boss Villain, but Her Strong Maternal Instincts Prevailed! – As Expected of a Former Single-Mom.',            'oel'),
		('baiyu',       'Bookstore with White Jade Wings',                                                                                                                                      'oel'),
		('electricity', 'Electric City’s Center for Lost Children',                                                                                                                             'oel'),
	
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	urlfrag = [
		('/baiyuyi-',      'Bookstore with White Jade Wings',                                                                                                                                 'oel'),
		('/cursed-',       'Kousei Ishikawa is Cursed!',                                                                                                                                      'oel'),
		('/wfb-chapter-',  'Wizard with the flower blades',                                                                                                                                   'oel'),
		('/senses-',       'Nai’s Five Senses',                                                                                                                                               'oel'),
		('/naissenses-',   'Nai’s Five Senses',                                                                                                                                               'oel'),
		('/assassin',      'The Former Assassin will Assassinate the Demon Generals because her Brother is the NPC Army’s Vice-Commander and the Heroes aren’t Leveling up Fast Enough',      'oel'),

	]

	for key, name, tl_type in urlfrag:
		if key in item['linkUrl'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
	return False