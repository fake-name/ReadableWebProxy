def extractSkythewood(item):
	"""
	# Skythewood translations

	"""
	
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	
	badwords = [
			'Drama CD',
			'Track',
		]
	if any([bad in item['title'] for bad in badwords]):
		return None

	badwords = [
			'Rant',
		]
	if any([bad in item['tags'] for bad in badwords]):
		return None



	tagmap = [
		('Five Days',                              'Unpopular As I Am, I Have To Meet a Heroine Within Five Days',                 'translated'),
		('Altina the Sword Princess',              'Haken no Kouki Altina',                                                        'translated'),
		('Overlord',                               'Overlord',                                                                     'translated'),
		('Gifting the wonderful world',            'Gifting the Wonderful World with Blessings!',                                  'translated'),
		('Alderamin',                              'Alderamin on the Sky',                                                         'translated'),
		("Knight's & Magic",                       "Knight's & Magic",                                                             'translated'),
		('Gate',                                   'Gate - Thus the JSDF Fought There!',                                           'translated'),
		('Genocide Reality',                       'Genocide Reality',                                                             'translated'),
		('Youjo Senki',                            'Youjo Senki',                                                                  'translated'),
		('Gifting',                                'Gifting the wonderful world with blessings!',                                  'translated'),
		('Killing Time of God',                    'Killing Time of God',                                                          'translated'),
		('Gamers',                                 'Gamers',                                                                       'translated'),
		('Manu',                                   'Manuscript Screening Boy and Manuscript Submitting Girl',                      'translated'),
		('Isekai Mahou',                           'Isekai Mahou wa Okureteru!',                                                   'translated'),
		('demon sword',                            'Demon Sword Master of the Holy Sword Academy',                                 'translated'),
		('lonely',                                 'Lonely Attack on the Different World',                                                   'translated'),
		('HWBT',                                   'Hero without Blood or Tear',                                                   'translated'),
		('Death',                                  'The Girl Raised by the Death God Holds the Sword of Darkness in Her Arms',     'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
	if item['title'].startswith('A Tale of Two Shadows'):
		return buildReleaseMessageWithType(item, 'A Tale of Two Shadows', vol, chp, frag=frag)
	if item['title'].startswith('The Legend of Faro: A Tale of Two Shadows Chapter'):
		return buildReleaseMessageWithType(item, 'A Tale of Two Shadows', vol, chp, frag=frag)
	if item['title'].startswith('Overlord'):
		return buildReleaseMessageWithType(item, 'Overlord', vol, chp, frag=frag)
	if item['title'].startswith('Hyperion 7'):
		return buildReleaseMessageWithType(item, 'Hyperion 7', vol, chp, frag=frag)
	if item['title'].startswith('I Want A Harem But She Is Very...'):
		return buildReleaseMessageWithType(item, 'I Want A Harem But She Is Very…', vol, chp, frag=frag)
	if item['title'].startswith('Gate of Twilight'):
		return buildReleaseMessageWithType(item, 'Gate of Twilight', vol, chp, frag=frag)
	if item['title'].startswith('Cooking with Wild Game Volume '):
		return buildReleaseMessageWithType(item, 'Cooking with Wild Game', vol, chp, frag=frag)
	return False