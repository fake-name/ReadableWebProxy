def extractDeadlynovelsTk(item):
	'''
	Parser for 'deadlynovels.tk'
	'''
	
	
	badwords = [
			'Talent System',
		]
	if any([bad in item['tags'] for bad in badwords]):
		return None

	if any([tmp.lower().endswith(" vip") for tmp in item['tags'] if tmp]):
		return None
	
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
		
		
		

	tagmap = [
		('Pirate in naruto world',              'Pirate in naruto world',                             'translated'),
		('One Piece Invincible',                'One Piece Invincible',                               'translated'),
		('The Mad Cultivator',                  'The Mad Cultivator',                                 'translated'),
		('Master of ninja world',               'Master of ninja world',                              'translated'),
		('My Fury Will Burn The Heavens',       'My Fury Will Burn The Heavens',                      'translated'),
		('Marvel Super Extraction',             'Marvel Super Extraction',                            'translated'),
		('One Piece Bounty System',             'One Piece Bounty System',                            'translated'),
		('Peerless Emporor System',             'Peerless Emporor System',                            'translated'),
		('Supreme Naruto',                      'Supreme Naruto',                                     'translated'),
		('System of Anger',                     'System of Anger',                                    'translated'),
		('Strongest Naruto System',             'Strongest Naruto System',                            'translated'),
		('Marvel: The King',                    'Marvel: The King',                                   'translated'),
		('Friendship System',                   'Friendship System',                                  'translated'),
		('One Piece system in Marvel world',    'One Piece system in Marvel world',                   'translated'),
		('Wants to die',                        'Wants to die',                                       'translated'),
		('One Piece Enhancement',               'One Piece Enhancement',                              'translated'),
		('I am Vegeta',                         'I am Vegeta',                                        'translated'),
		('Marvel Happy system',                 'Marvel Happy system',                                'translated'),
		('Source System Naruto',                'Source System Naruto',                               'translated'),
		('Dragon Ball : Broly',                 'Dragon Ball : Broly',                                'translated'),
		('Scientist to God',                    'Scientist to God',                                   'translated'),
		('One Piece Infinity Gloves',           'One Piece Infinity Gloves',                          'translated'),
		('Pervert in One Piece World',          'Pervert in One Piece World',                         'translated'),
		('One Piece: Shendu',                   'One Piece: Shendu',                                  'translated'),
		('one piece devil',                     'One Piece Devil',                                    'translated'),
		('Super Demon',                         'Super Demon',                                        'translated'),
		('son of whitebeard',                   'Son of Whitebeard',                                  'translated'),
		('marvel card system',                  'Marvel Card System',                                 'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False