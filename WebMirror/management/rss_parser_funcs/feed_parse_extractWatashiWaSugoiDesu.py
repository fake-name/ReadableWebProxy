def extractWatashiWaSugoiDesu(item):
	'''
	Parser for 'Watashi wa Sugoi Desu'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Violant of the Silver',                           'Violant of the Silver',                                                                                         'translated'),
		('dolls',                                           'I Decided to Not Compete and Quietly Create Dolls Instead',                                                     'translated'),
		('But You Said You\'d Give Me Delicious Candy!!',   'But You Said You\'d Give Me Delicious Candy!!',                                                                 'translated'),
		('Kokkuri-san',                                     'But You Said You\'d Give Me Delicious Candy!!',                                                                 'translated'),
		('Cute Friend',                                     'The Hero’s Cute Childhood Friend, Doesn’t Know of His Pitch-Black Nature',                                      'translated'),
		('TS Girl',                                         'My Best Friend Became A Transsexual Girl, And Says He Wants to Marry Me, But I’ll Flat Out Refuse.',            'translated'),
		('SFY',                                             'Searching For You',                                                                                             'translated'),
		('smgo',                                            'The Show Must Go On',                                                                                           'translated'),
		('wsbw',                                            'When She Becomes a Witch',                                                                                      'translated'),
		('gdg',                                             'The Gentle Death God Laughs Above the Cherry-Blossom Sky',                                                      'translated'),
		('KtBC',                                            'Kiss the Black Cat',                                                                                            'translated'),
		('Ossan Idol',                                      'Ossan (36) Ga Idol Ni Naru Hanashi',                                                                            'translated'),
		('Strongest Wiseman',                               'Child Rearing Journal of the Strongest Wiseman～About My Daughter Being the Cutest in the World～',             'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	titlemap = [
		('Child Rearing Journal of the Strongest Wiseman～About My Daughter Being the Cutest in the World～',  'Child Rearing Journal of the Strongest Wiseman～About My Daughter Being the Cutest in the World～',      'translated'), 
		('Ossan Idol : Chapter',                                                                          'Ossan (36) Ga Idol Ni Naru Hanashi',                                                                     'translated'), 
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	return False