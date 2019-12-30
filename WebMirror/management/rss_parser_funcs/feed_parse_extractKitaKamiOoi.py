def extractKitaKamiOoi(item):
	"""
	'KitaKami Ooi'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	tagmap = [
		('Escaping the Nuclear Fallout Shelter that has Turned Into a Dungeon Alone?', 'Escaping the Nuclear Fallout Shelter that has Turned Into a Dungeon Alone?', 'translated'),
		('Otome Game Rokkushuume, Automode ga Kiremashita',                            'Otome Game Rokkushuume, Automode ga Kiremashita',                            'translated'),
		('Akuyaku Reijou wa Ringoku no Oitaishi ni Dekiai Sareru',                     'Akuyaku Reijou wa Ringoku no Oitaishi ni Dekiai Sareru',                     'translated'),
		('Akuyaku Reijou wa Ringoku no Outaishi ni Dekiai Sareru',                     'Akuyaku Reijou wa Ringoku no Oitaishi ni Dekiai Sareru',                     'translated'),
		('Skill Up with Login Bonus',                                                  'Skill Up with Login Bonus',                                                  'translated'),
		('Watashi wa Teki ni Narimasen!',                                              'Watashi wa Teki ni Narimasen!',                                              'translated'),
		('I Chose to Fake My Death',                                                   'I Chose to Fake My Death',                                                   'translated'),
		('Chuunibyou Demo Koi ga Shitai!',                                             'Chuunibyou Demo Koi ga Shitai!',                                             'translated'),
		('Gomen ne Onii-sama',                                                         'Gomen ne Onii-sama',                                                         'translated'),
		('My Girlfriend Lulu',                                                         'My Girlfriend Lulu',                                                         'translated'),
		('I Decided to Not Compete and Quietly Create Dolls Instead',                  'I Decided to Not Compete and Quietly Create Dolls Instead',                  'translated'),
		('B.A.D.',                                                                     'B.A.D.',                                                                     'translated'),
		('Beyond Another Darkness',                                                    'B.A.D.',                                                                     'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
	return False