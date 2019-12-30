def extractKillerNinjaScrapBook(item):
	'''
	Parser for 'Killer Ninja  Scrap  Book'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	titlemap = [
		('A Mistaken Marriage Match: Pirate’s Daughter Volume',     'A Mistaken Marriage Match: Pirates Daughter',                        'translated'),
		('	A Mistaken Marriage Match: Pirate’s Daughter ',         'A Mistaken Marriage Match: Pirates Daughter',                        'translated'),
		('A Mistaken Marriage Match 4',                             'A Mistaken Marriage Match: Pirates Daughter',                        'translated'),
		('A Mistaken Marriage Match 4 Pirate’s Daughter',           'A Mistaken Marriage Match: Pirates Daughter',                        'translated'),
		('A Mistaken Marriage Match 4: The Pirate’s Daughter',      'A Mistaken Marriage Match: Pirates Daughter',                        'translated'),
		('Mysteries in the Imperial Harem:',                        'A Mistaken Marriage Match: Mysteries in the Imperial Harem',         'translated'),
		('A Mistaken Marriage Match2:',                             'A Mistaken Marriage Match: A Generation of Military Counselor',      'translated'),
		('Pursuit of Murderer in Liao Yue',                         'A Mistaken Marriage Match: Pursuit of Murderer in Liao Yue',         'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



	urlfrag = [
		('/a-mistaken-marriage-4-pirates-daughter', 'A Mistaken Marriage Match: Pirates Daughter',                       'translated'),
		('/a-mistaken-marriage-match-4-',           'A Mistaken Marriage Match: Pirates Daughter',                       'translated'),
		('/a-mistaken-marriage-match-2-',           'A Mistaken Marriage Match: A Generation of Military Counselor',     'translated'),
		('/a-mistaken-marriage-match2-',            'A Mistaken Marriage Match: A Generation of Military Counselor',     'translated'),
		('/a-mistaken-marriage-match2generation',   'A Mistaken Marriage Match: A Generation of Military Counselor',     'translated'),

	]

	for key, name, tl_type in urlfrag:
		if key in item['linkUrl'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



	return False