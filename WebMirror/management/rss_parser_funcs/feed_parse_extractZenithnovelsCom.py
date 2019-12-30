def extractZenithnovelsCom(item):
	'''
	Parser for 'zenithnovels.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Blade Online',                                           'Blade Online',                                            'translated'),
		('The Great Conqueror',                                    'The Great Conqueror',                                     'translated'),
		('The Crimson Dragon',                                     'The Crimson Dragon',                                      'translated'),
		('Paranormal World (The Semi-Physical World)',             'Paranormal World (The Semi-Physical World)',              'translated'), 
		('It’s Impossible that My Evil Overlord is So Cute',       'It’s Impossible that My Evil Overlord is So Cute',        'translated'), 
		('Returning from the Immortal World',                      'Returning from the Immortal World',                       'translated'), 
		('Tsuki ga Michibiku Isekai Douchuu (POV)',                'Tsuki ga Michibiku Isekai Douchuu',                       'translated'), 
		('Starchild Escapes Arranged Marriage',                    'Starchild Escapes Arranged Marriage',                     'translated'), 
		('The Lame Daoist Priest',                                 'The Lame Daoist Priest',                                  'translated'), 
		('Headless Dullahan',                                      'I\'m a Dullahan, Looking for My Head',                    'translated'), 
		('Higawari Teni ~ Ore wa Arayuru Sekai de Musou Suru ~',   'Higawari Teni ~ Ore wa Arayuru Sekai de Musou Suru ~',    'translated'), 
		('Godly Student',                                          'Godly Student',                                           'translated'), 
		('Infinity Armament',                                      'Infinity Armament',                                       'translated'), 
		('Evil-like Duke Household',                               'Evil-like Duke Household',                                'translated'), 
		('Omae Mitai na Hiroin ga Ite Tamaruka!',                  'Omae Mitai na Hiroin ga Ite Tamaruka!',                   'translated'), 
		('Starting From Zero',                                     'Starting From Zero',                                      'translated'), 
		('M E M O R I Z E',                                        'M E M O R I Z E',                                         'translated'), 
		('The World That Tao Rules',                               'The World That Tao Rules',                                'translated'), 
		('Supreme Arrow God',                                      'Supreme Arrow God',                                       'translated'), 
		('The God of Sky & Earth',                                 'The God of Sky & Earth',                                  'translated'), 
		('Eternal Martial Emperor',                                'Eternal Martial Emperor',                                 'translated'), 
		('The Great Merchant in the Cataclysm',                    'The Great Merchant in the Cataclysm',                     'translated'), 
		('Amaku Yasashii Sekai de Ikiru ni wa',                    'Amaku Yasashii Sekai de Ikiru ni wa',                     'translated'), 
		('I\'m the Boss Who Modified the World',                   'I\'m the Boss Who Modified the World',                    'translated'), 
		('Can I Survive More than 3 Chapters?',                    'Can I Survive More than 3 Chapters?',                     'translated'), 
		('ten thousand paths to becoming a god',                   'Ten Thousand Paths to Becoming a God',                    'translated'), 
		('urban carefree immortal emperor',                        'urban carefree immortal emperor',                         'translated'), 
		('the deity of war',                                       'the deity of war',                                        'translated'), 
		('The Almighty Asura',                                     'The Almighty Asura',                                      'translated'), 
		('The Hunter Under the Tree of Origin',                    'The Hunter Under the Tree of Origin',                     'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			if 'Tsuki ga Michibiku Isekai Douchuu (POV)' in item['tags']:
				postfix = "POV Chapter"
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	return False