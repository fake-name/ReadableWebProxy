def extractOniichanyamete(item):
	"""
	お兄ちゃん、やめてぇ！ / Onii-chan Yamete
	"""
	
	if 'Manga' in item['tags']:
		return None
	
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
		
	tagmap = [
		('The Bathroom Goddess',                  'The Bathroom Goddess',                              'translated'),
		('a wild boss appeared',                  'A Wild Boss Appeared',                              'translated'),
		('The Girl Who Bore the Flame Ring',      'The Girl Who Bore the Flame Ring',                  'translated'),
		('Debt Girl',                             'The Noble Girl Living in Debt',                     'translated'),
		("I'm the Final Boss!?",                  "I'm the Final Boss!?",                              'oel'),
		('Tiger Story',                           'Tiger Story',                                       'oel'),
		('Vampire Nap',                           'The Reincarnated Vampire Wants an Afternoon Nap',   'translated'),
		('Haunted',                               'Haunted Duke’s Daughter',                           'translated'),
		('The Cute Cook',                         'The Cute Cook',                                     'translated'),
		('demon maid',                            'Miss Demon Maid',                                           'translated'),
		('Arachne',                               'Arachne',                                           'translated'),
		('bunny girl',                            'Apotheosis of a Demon – A Monster Evolution Story', 'translated'),
		('Kunoichi',                              'The Pseudo-Kunoichi from Another World',            'translated'),
		
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	if 'Jashin Average' in item['title'] or 'Cthulhu Average' in item['title'] or 'Evil God Average' in item['tags'] or 'jashin' in item['tags']:
		return buildReleaseMessageWithType(item, 'Evil God Average', vol, chp, frag=frag, postfix=postfix)
	if 'Tilea’s Worries' in item['title']:
		return buildReleaseMessageWithType(item, "Tilea's Worries", vol, chp, postfix=postfix)
	if 'Tilea' in item['tags'] and 'Raid on the Capital' in item['title'] and not vol:
		return buildReleaseMessageWithType(item, "Tilea's Worries", 2, chp, postfix=postfix)
	if 'Tilea' in item['tags'] and 'Turf War' in item['title'] and not vol:
		return buildReleaseMessageWithType(item, "Tilea's Worries", 3, chp, postfix=postfix)
	if 'Kenkyo Kenjitu' in item['tags'] or 'Reika-sama' in item['title']:
		return buildReleaseMessageWithType(item, 'Kenkyo Kenjitu', vol, chp, postfix=postfix)
	if 'My Sister the Heroine and I the Villainess' in item['tags']:
		return buildReleaseMessageWithType(item, 'My Sister the Heroine, and I the Villainess', vol, chp, postfix=postfix)
	if 'I’m Back in the Other World' in item['title']:
		return buildReleaseMessageWithType(item, "I'm Back in the Other World", vol, chp)
	if 'Kazuha Axeplant’s Third Adventure:' in item['title']:
		return buildReleaseMessageWithType(item, "Kazuha Axeplant's Third Adventure", vol, chp)
	elif 'otoburi' in item['tags'] or 'Otoburi' in item['tags']:
		volume_lut = {'3 years old': 1, '5 years old': 1, '6 years old': 1, '7 years old': 1, '12 years old': 1, '14 years old': 1, '15 years old': 1, '16 years old': 1,
		    'School Entrance Ceremony': 2, 'First Year First Semester': 2, '1st Year 1st Semester': 2, 'Summer Vacation': 3, 'Summer Vacation 2nd Half': 3,
		    'Summer Vacation Last': 3, 'First Year Second Semester': 4, 'Recuperating?': 5, 'Wedding Preparations?': 5, 'Newlywed Life': 5, 'Cleanup': 6,
		    'My Lord’s Engagement': 6, 'The Winter is Almost Here': 6, 'Experiments and Preparations': 6, 'Engagement Party': 6, 'In the Middle of a Fight?': 7,
		    'In the Middle of Reflecting': 7}
		for chp_key in volume_lut.keys():
			if chp_key.lower() in item['title'].lower():
				return buildReleaseMessageWithType(item, 'Otome Game no Burikko Akuyaku Onna wa Mahou Otaku ni Natta', volume_lut[chp_key], chp)
	return False